# Plan: Version Support and Time Scaling Features

## 1. Version Support Enhancement

### Objective
Add robust support for different Camtasia .tscproj format versions, with graceful handling of unsupported older formats.

### Analysis of Version Differences

Based on the format documentation and example files:

#### Version 4.0 (Camtasia 2020 and earlier)
- `editRate`: 60 (simple ticks per second)
- Time values are simple integers
- Simpler project structure
- Less precise timing

#### Version 9.0 (Camtasia 2021+)
- `editRate`: 705600000 (high precision)
- More complex time representation
- Additional properties like `allowSubFrameEditing`
- More media types and effects

### Implementation Strategy

#### 1.1 Version Detection
```python
def detect_version(data: dict) -> tuple[str, int]:
    """Detect project version and edit rate."""
    version = data.get('version', '4.0')
    edit_rate = data.get('editRate', 60)
    
    # Validate known versions
    if version not in ['4.0', '9.0']:
        logger.warning(f"Unknown version {version}, attempting to process")
    
    return version, edit_rate
```

#### 1.2 Version Compatibility Layer
- Create a `VersionHandler` class that normalizes differences
- For very old versions (< 4.0), log error and refuse to process
- For unknown versions, attempt processing with warnings

#### 1.3 Properties to Handle by Version
- **Version 4.0**: Basic scaling only
- **Version 9.0**: Full feature support including sub-frame editing

### Error Handling
```python
if version < '4.0':
    logger.error(f"File format version {version} is too old and not supported. Please upgrade your Camtasia project.")
    raise ValueError(f"Unsupported version: {version}")
```

## 2. Time Scaling Operation

### Objective
Implement a `timescale` command that scales all time-related properties in a project, effectively changing the playback speed.

### Key Considerations
- Scale all timing properties (start, duration, mediaStart, mediaDuration)
- Scale keyframe times
- Scale transition durations
- **DO NOT** scale audio clip durations (preserve audio integrity)
- Reposition audio clips according to the time stretch

### Implementation Design

#### 2.1 Time Properties to Scale

**Always Scale:**
- `start` - Timeline position
- `duration` - Clip duration on timeline (except for audio)
- `mediaStart` - Start point within source
- `mediaDuration` - Duration from source (except for audio)
- `endTime` - Keyframe end times
- `time` - Keyframe times
- Transition durations
- `range` values in source tracks

**Never Scale:**
- `editRate` - Project time base
- `videoFormatFrameRate` - Target frame rate
- `audioFormatSampleRate` - Audio sample rate
- Audio track durations (preserve audio playback speed)

#### 2.2 Audio Handling Strategy

For audio clips (AMFile, audio tracks in UnifiedMedia):
1. Scale the `start` position (reposition in timeline)
2. Keep `duration` unchanged (preserve audio length)
3. Scale any fade in/out keyframes
4. Adjust subsequent clips to prevent overlaps

```python
def scale_audio_timing(media: dict, scale_factor: float) -> dict:
    """Scale audio timing while preserving duration."""
    if 'start' in media:
        media['start'] = int(media['start'] * scale_factor)
    
    # Duration remains unchanged for audio
    # But scale any volume keyframes
    if 'parameters' in media and 'volume' in media['parameters']:
        scale_keyframe_times(media['parameters']['volume'], scale_factor)
    
    return media
```

#### 2.3 Time Scaler Class

```python
class TimeScaler(TscprojScaler):
    """Handles time scaling of Camtasia projects."""
    
    # Time properties to scale
    TIME_PROPERTIES = {
        'start', 'duration', 'mediaStart', 'mediaDuration',
        'endTime', 'time', 'range'
    }
    
    # Properties to skip for audio
    AUDIO_SKIP_PROPERTIES = {'duration', 'mediaDuration'}
    
    def _is_audio_media(self, media: dict) -> bool:
        """Check if media is audio-only."""
        media_type = media.get('_type', '')
        return media_type == 'AMFile' or (
            media_type == 'UnifiedMedia' and 
            'audio' in media and 'video' not in media
        )
```

### CLI Interface

```bash
# Speed up to 150% (1.5x faster)
tscprojpy timescale --input project.tscproj --scale 150.0

# Slow down to 75% (0.75x speed)
tscprojpy timescale --input project.tscproj --scale 75.0

# With custom output
tscprojpy timescale --input project.tscproj --scale 200.0 --output fast_version.tscproj
```

### Algorithm Overview

1. **Load and validate project**
   - Check version compatibility
   - Determine edit rate

2. **Scale time properties**
   - Traverse entire project structure
   - Identify time-related properties
   - Apply scaling based on media type

3. **Handle special cases**
   - Audio clips: reposition but don't stretch
   - Keyframes: scale all time values
   - Transitions: scale durations
   - Source ranges: scale for video, preserve for audio

4. **Validate result**
   - Ensure no negative times
   - Check for timeline conflicts
   - Verify audio positioning

### Edge Cases to Handle

1. **Overlapping clips after scaling**
   - Detect and warn about overlaps
   - Optionally auto-adjust positions

2. **Fractional frame times**
   - Round to nearest valid frame time
   - Respect `allowSubFrameEditing` setting

3. **Mixed media (UnifiedMedia)**
   - Scale video portion normally
   - Preserve audio duration
   - Maintain sync between tracks

## 3. Integration Plan

### Phase 1: Version Support (1 week)
- [ ] Add version detection to scaler.py
- [ ] Create VersionHandler class
- [ ] Add compatibility warnings
- [ ] Test with files from different versions
- [ ] Update documentation

### Phase 2: Time Scaling Core (1 week)
- [ ] Create TimeScaler class inheriting from TscprojScaler
- [ ] Implement time property detection
- [ ] Add audio media detection logic
- [ ] Implement differential scaling for audio
- [ ] Add time validation functions

### Phase 3: CLI Integration (3 days)
- [ ] Add timescale command to cli.py
- [ ] Implement mutual exclusivity with xyscale
- [ ] Add appropriate help text
- [ ] Test command-line interface

### Phase 4: Testing & Edge Cases (1 week)
- [ ] Create comprehensive test suite
- [ ] Test with various project types
- [ ] Handle edge cases (overlaps, precision)
- [ ] Performance testing with large projects

### Phase 5: Documentation (2 days)
- [ ] Update README with timescale examples
- [ ] Document version compatibility
- [ ] Add troubleshooting guide
- [ ] Update CHANGELOG

## 4. Technical Considerations

### Performance
- Time scaling is computationally similar to spatial scaling
- Large projects may have thousands of keyframes
- Consider progress reporting for long operations

### Precision
- Maintain numeric precision for time values
- Consider edit rate when rounding
- Preserve fractional times where supported

### Validation
- Ensure timeline integrity after scaling
- Detect impossible scenarios (negative durations)
- Warn about potential audio sync issues

## 5. Future Enhancements

1. **Smart overlap resolution**
   - Automatically adjust clips to prevent overlaps
   - Maintain relative spacing

2. **Pitch preservation for audio**
   - Optional audio time-stretching with pitch correction
   - Requires external audio processing

3. **Selective time scaling**
   - Scale only specific tracks or time ranges
   - Useful for complex edits

4. **Frame rate conversion**
   - Adjust project frame rate with proper scaling
   - Handle frame rate mismatches

## 6. Success Criteria

- Version detection works for all example files
- Old version files show clear error messages
- Time scaling produces valid, playable projects
- Audio remains at original speed but repositioned correctly
- All keyframes and transitions scale properly
- No data loss or corruption
- Clear documentation and examples