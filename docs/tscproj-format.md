# Camtasia .tscproj File Format Documentation

## Overview

The `.tscproj` file is the project file format used by TechSmith Camtasia, a screen recording and video editing software. These files are stored in JSON format and contain all the information needed to reconstruct a video editing project, including media references, timeline structure, effects, and project settings.

## File Structure

A `.tscproj` file has the following top-level structure:

```json
{
  "title": "",
  "description": "",
  "author": "",
  "targetLoudness": -18.0,
  "shouldApplyLoudnessNormalization": true,
  "videoFormatFrameRate": 60,
  "audioFormatSampleRate": 44100,
  "allowSubFrameEditing": false,
  "width": 1280.0,
  "height": 720.0,
  "version": "9.0",
  "editRate": 705600000,
  "authoringClientName": {...},
  "sourceBin": [...],
  "timeline": {...}
}
```

## Root-Level Properties

### Project Metadata
- **`title`** (string): Project title
- **`description`** (string): Project description
- **`author`** (string): Project author

### Canvas Settings
- **`width`** (float): Canvas width in pixels
- **`height`** (float): Canvas height in pixels

### Audio/Video Settings
- **`videoFormatFrameRate`** (integer): Target frame rate (e.g., 30, 60)
- **`audioFormatSampleRate`** (integer): Audio sample rate in Hz (e.g., 44100, 48000)
- **`targetLoudness`** (float): Target loudness in LUFS (typically -18.0)
- **`shouldApplyLoudnessNormalization`** (boolean): Whether to apply loudness normalization
- **`allowSubFrameEditing`** (boolean): Whether sub-frame editing is allowed

### Technical Properties
- **`version`** (string): Project format version (e.g., "4.0", "9.0")
- **`editRate`** (integer): Edit rate/time base (varies by version)
  - Older versions: 60 (ticks per second)
  - Newer versions: 705600000 (higher precision time base)
- **`authoringClientName`** (object): Information about the Camtasia version
  ```json
  {
    "name": "Camtasia",
    "platform": "Mac" | "Windows",
    "version": "2025.1.4"
  }
  ```

## Source Media (sourceBin)

The `sourceBin` array contains all media files imported into the project:

```json
"sourceBin": [
  {
    "id": 1,
    "src": "./media/1752976336.728338/filename.mp4",
    "rect": [0, 0, 1920, 1080],
    "lastMod": "20250419T143221",
    "loudnessNormalization": true,
    "sourceTracks": [...],
    "metadata": {...}
  }
]
```

### Source Item Properties
- **`id`** (integer): Unique identifier for this source
- **`src`** (string): Relative path to the media file
- **`rect`** (array[4]): Bounding rectangle [x, y, width, height]
- **`lastMod`** (string): Last modification timestamp (ISO format)
- **`loudnessNormalization`** (boolean): Audio normalization setting

### Source Tracks

Each source item contains `sourceTracks` describing the media streams:

```json
"sourceTracks": [
  {
    "range": [0, 9817],
    "type": 0,
    "editRate": 1000,
    "trackRect": [0, 0, 1280, 720],
    "sampleRate": 60,
    "bitDepth": 0,
    "numChannels": 0,
    "integratedLUFS": 100.0,
    "peakLevel": -1.0,
    "tag": 0,
    "metaData": "...",
    "parameters": {}
  }
]
```

#### Track Type Values
- **`type: 0`**: Video track
- **`type: 1`**: Image/still track
- **`type: 2`**: Audio track

## Timeline Structure

The timeline contains the actual edit information:

```json
"timeline": {
  "id": 22,
  "sceneTrack": {
    "scenes": [
      {
        "csml": {
          "tracks": [...]
        }
      }
    ]
  }
}
```

### Track Structure

Each track in the timeline contains media items:

```json
{
  "trackIndex": 0,
  "medias": [...],
  "parameters": {},
  "ident": "",
  "audioMuted": false,
  "videoHidden": false,
  "magnetic": false,
  "matte": 0,
  "solo": false,
  "metadata": {
    "IsLocked": "False",
    "trackHeight": "54"
  }
}
```

## Media Types

Media items on the timeline have different `_type` values:

### Video Media Types
- **`VMFile`**: Video Media File - references video from sourceBin
- **`ScreenVMFile`**: Screen recording video file
- **`IMFile`**: Image Media File - for still images
- **`UnifiedMedia`**: Combined video and audio media

### Audio Media Types
- **`AMFile`**: Audio Media File

### Annotation Types
- **`Callout`**: Callout/annotation object
- **`Group`**: Group of media items

### Common Media Properties

```json
{
  "id": 25,
  "_type": "VMFile",
  "src": 1,  // References sourceBin ID
  "trackNumber": 0,
  "attributes": {
    "ident": "clip_name"
  },
  "parameters": {
    "translation0": 0.0,    // X position
    "translation1": 0.0,    // Y position
    "scale0": 1.0,          // X scale
    "scale1": 1.0,          // Y scale
    "rotation0": 0.0,       // X rotation
    "rotation1": 0.0,       // Y rotation
    "rotation2": 0.0,       // Z rotation
    "geometryCrop0": 0.0,   // Left crop
    "geometryCrop1": 0.0,   // Top crop
    "geometryCrop2": 0.0,   // Right crop
    "geometryCrop3": 0.0,   // Bottom crop
    "opacity": 1.0
  },
  "effects": [],
  "start": 164640000,
  "duration": 1081920000,
  "mediaStart": 4727520000,
  "mediaDuration": 1081920000,
  "scalar": 1,
  "metadata": {...},
  "animationTracks": {...}
}
```

## Timing and Duration

Time values in the project are represented differently based on the version:

- **Older versions**: Time in ticks (60 ticks per second)
- **Newer versions**: Time in high-precision units (editRate-based)

Common time-related properties:
- **`start`**: Start time on timeline
- **`duration`**: Duration on timeline
- **`mediaStart`**: Start point within source media
- **`mediaDuration`**: Duration from source media

## Keyframe Animation

Animated properties use keyframes:

```json
"scale0": {
  "type": "double",
  "defaultValue": 1.0,
  "keyframes": [
    {
      "endTime": 58800000,
      "time": 11760000,
      "value": 0.444444444444444,
      "interp": "linr",
      "duration": 47040000
    }
  ]
}
```

### Keyframe Properties
- **`time`**: Keyframe time
- **`endTime`**: End time of this keyframe segment
- **`value`**: Value at this keyframe
- **`interp`**: Interpolation type ("linr" = linear)
- **`duration`**: Duration to next keyframe

## Callout Objects

Callouts are annotation objects with special properties:

```json
{
  "_type": "Callout",
  "def": {
    "kind": "remix",
    "shape": "shape-rectangle",
    "style": "basic",
    "corner-radius": 8.0,
    "fill-color-red": 0.0,
    "fill-color-green": 0.0,
    "fill-color-blue": 0.0,
    "fill-color-opacity": 1.0,
    "stroke-color-red": 1.0,
    "stroke-color-green": 1.0,
    "stroke-color-blue": 1.0,
    "stroke-color-opacity": 1.0,
    "stroke-width": 0.0,
    "width": 240.0,
    "height": 180.0,
    "fill-style": "solid",
    "stroke-style": "solid"
  }
}
```

## Effects and Transitions

Effects are stored in the `effects` array of media items:

```json
"effects": [
  {
    "name": "Effect Name",
    "parameters": {...}
  }
]
```

Transitions between clips are stored in a `transitions` array:

```json
"transitions": [
  {
    "name": "Glitch",
    "duration": 294000000,
    "rightMedia": 36,
    "attributes": {
      "Random": 0.0,
      "bypass": false,
      "reverse": false
    }
  }
]
```

## Version Differences

### Camtasia 2020 and Earlier
- Version: "4.0"
- Edit rate: 60
- Simpler time representation

### Camtasia 2021 and Later
- Version: "9.0"
- Edit rate: 705600000
- High-precision time values
- Additional properties like `allowSubFrameEditing`

## File References

All media files are referenced relative to the project file location, typically in a `media/` subdirectory with timestamp-based folders:

```
./media/1752976336.728338/filename.mp4
```

## Best Practices for Parsing

1. **Version Checking**: Always check the `version` field to handle format differences
2. **Time Conversion**: Be aware of different `editRate` values when calculating times
3. **Media References**: Handle missing media files gracefully
4. **Property Types**: Some numeric properties may be stored as strings (e.g., fractions like "2997/100")
5. **Optional Properties**: Not all properties are present in all files

## Common Use Cases

### Scaling a Project
When scaling a project (like changing from 1080p to 4K), modify:
- Root `width` and `height`
- All `rect` and `trackRect` arrays
- Position properties (`translation0`, `translation1`)
- Size properties (`scale0`, `scale1`, `width`, `height` in definitions)
- Keyframe values for animated properties

### Finding Media Duration
To calculate actual duration in seconds:
```
duration_seconds = duration / editRate
```

### Media Type Detection
- Check `numChannels > 0` for audio tracks
- Check `trackRect` dimensions for video tracks
- `type` field indicates track type (0=video, 1=image, 2=audio)