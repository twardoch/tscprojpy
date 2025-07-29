# Camtasia .tscproj Format Specification

## TL;DR

The `.tscproj` file is Camtasia's project file format stored as JSON. It contains:
- **Canvas dimensions** (`width`, `height`) and project settings
- **Source media** (`sourceBin`) - all imported files with metadata  
- **Timeline structure** (`timeline`) - scenes, tracks, and media clips
- **Media transformations** - position, scale, rotation, opacity
- **Animations** - keyframe-based property changes over time
- **Effects and transitions** - visual/audio effects between clips

Key scaling properties include:
- Root `width`/`height` for canvas
- `rect` arrays `[x, y, width, height]` for media bounds
- `translation0`/`translation1` for X/Y positioning
- `scale0`/`scale1` for X/Y scaling factors
- Keyframe values for animated properties

## Table of Contents

1. **@01-overview.md** - General Structure and Purpose
   - JSON structure overview
   - Main components (root, sourceBin, timeline)
   - File references and paths
   - Use cases and applications

2. **@02-root-properties.md** - Root Level Properties
   - Project metadata (title, author, description)
   - Canvas dimensions and aspect ratio
   - Frame rate and audio settings
   - Version and authoring client info
   - Edit rate and time representation

3. **@03-source-media.md** - Source Media Management
   - sourceBin structure and organization
   - Media file references and paths
   - Source tracks (video, audio, image)
   - Track types and metadata
   - Loudness normalization settings

4. **@04-timeline-structure.md** - Timeline Organization
   - Scene track hierarchy
   - Track indices and layering
   - Media clip placement
   - Track parameters and settings
   - Magnetic tracks and locking

5. **@05-media-types.md** - Media Item Types
   - Video types (VMFile, ScreenVMFile, UnifiedMedia)
   - Audio types (AMFile)
   - Image types (IMFile)
   - Annotation types (Callout, Group)
   - Text and shape callouts

6. **@06-animation-keyframes.md** - Animation System
   - Keyframe structure and properties
   - Interpolation types
   - Animated parameters
   - Time representation in keyframes
   - Animation tracks

7. **@07-effects-transitions.md** - Effects and Transitions
   - Effect application and parameters
   - Transition types and duration
   - Audio and visual pre-roll
   - Effect attributes
   - Transition placement

8. **@08-positioning-scaling.md** - Coordinate Systems
   - Canvas coordinate system
   - Rectangle arrays (rect, trackRect)
   - Translation and positioning
   - Scale factors and transformations
   - Rotation (X, Y, Z axes)
   - Geometry cropping
   - Opacity and blending

9. **@09-version-differences.md** - Version Compatibility
   - Version 4.0 (Camtasia 2020 and earlier)
   - Version 9.0 (Camtasia 2021+)
   - Edit rate differences
   - Time representation changes
   - Feature additions by version
   - Backward compatibility considerations

## Quick Reference

### Essential Properties for Scaling
```json
{
  "width": 1920.0,           // Canvas width
  "height": 1080.0,          // Canvas height
  "sourceBin": [{
    "rect": [0, 0, 1920, 1080],  // Source bounds
    "trackRect": [0, 0, 1920, 1080]  // Track bounds
  }],
  "timeline": {
    "tracks": [{
      "medias": [{
        "parameters": {
          "translation0": 0.0,   // X position
          "translation1": 0.0,   // Y position
          "scale0": 1.0,         // X scale
          "scale1": 1.0          // Y scale
        }
      }]
    }]
  }
}
```

### Version Detection
- **Version 4.0**: `editRate: 60`
- **Version 9.0**: `editRate: 705600000`