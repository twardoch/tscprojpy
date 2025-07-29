# Media Item Types

Media items are the individual clips, images, audio files, and annotations placed on the timeline. Each media type has specific properties and behaviors.

## Common Media Properties

All media items share these base properties:

```json
{
  "id": 25,
  "_type": "VMFile",
  "src": 1,  // References sourceBin ID
  "trackNumber": 0,
  "attributes": {
    "ident": "clip_name"
  },
  "parameters": {...},
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

### Core Properties

#### `id` (integer)
- **Description**: Unique identifier for this media item
- **Required**: Yes
- **Note**: Must be unique across entire timeline

#### `_type` (string)
- **Description**: Media type identifier
- **Required**: Yes
- **Values**: See media types below

#### `src` (integer)
- **Description**: Source media ID from sourceBin
- **Required**: Yes (except for generated content)
- **Note**: References `sourceBin[].id`

#### `trackNumber` (integer)
- **Description**: Source track to use (for multi-track sources)
- **Default**: `0`
- **Example**: `0` for video, `1` for audio in same file

### Timing Properties

#### `start` (integer)
- **Description**: Position on timeline
- **Units**: Project edit rate units
- **Required**: Yes

#### `duration` (integer)
- **Description**: Length on timeline
- **Units**: Project edit rate units
- **Required**: Yes

#### `mediaStart` (integer)
- **Description**: In-point within source media
- **Units**: Source media edit rate units
- **Default**: `0`

#### `mediaDuration` (integer)
- **Description**: Length of source media used
- **Units**: Source media edit rate units
- **Default**: Same as `duration`

#### `scalar` (integer)
- **Description**: Playback speed multiplier
- **Default**: `1`
- **Examples**: `2` = double speed, `0.5` = half speed

## Video Media Types

### VMFile (Video Media File)
```json
{
  "_type": "VMFile",
  "src": 1,
  "parameters": {
    "translation0": 0.0,    // X position
    "translation1": 0.0,    // Y position
    "scale0": 1.0,          // X scale
    "scale1": 1.0,          // Y scale
    "rotation0": 0.0,       // X rotation
    "rotation1": 0.0,       // Y rotation
    "rotation2": 0.0,       // Z rotation
    "opacity": 1.0
  }
}
```

### ScreenVMFile (Screen Recording)
```json
{
  "_type": "ScreenVMFile",
  "src": 2,
  "parameters": {
    // Same as VMFile
  },
  "systemAudioOffset": 0  // Audio sync offset
}
```

### UnifiedMedia (Combined Video/Audio)
```json
{
  "_type": "UnifiedMedia",
  "video": {
    "id": 16,
    "_type": "ScreenVMFile",
    "src": 1,
    "trackNumber": 1,
    // Video properties
  },
  "audio": {
    "id": 17,
    "_type": "AMFile",
    "src": 1,
    "trackNumber": 0,
    // Audio properties
  }
}
```

## Audio Media Types

### AMFile (Audio Media File)
```json
{
  "_type": "AMFile",
  "src": 3,
  "trackNumber": 0,
  "attributes": {
    "ident": "background_music",
    "gain": 1.0,
    "mixToMono": false,
    "loudnessNormalization": true,
    "sourceFileOffset": 0
  },
  "channelNumber": "0,1",  // Stereo channels
  "parameters": {
    "volume": 1.0  // Can be animated
  }
}
```

#### Audio-Specific Attributes
- **`gain`** (float): Audio gain multiplier
- **`mixToMono`** (boolean): Convert to mono
- **`loudnessNormalization`** (boolean): Apply normalization
- **`sourceFileOffset`** (integer): Offset in source file

## Image Media Types

### IMFile (Image Media File)
```json
{
  "_type": "IMFile",
  "src": 4,
  "parameters": {
    "translation0": 100.0,
    "translation1": 50.0,
    "scale0": 0.5,
    "scale1": 0.5,
    "opacity": 0.8
  }
}
```

## Annotation Types

### Callout
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
    "stroke-width": 3.0,
    "width": 240.0,
    "height": 180.0,
    "fill-style": "solid",
    "stroke-style": "solid"
  }
}
```

### Text Callout
```json
{
  "_type": "Callout",
  "def": {
    "kind": "remix",
    "shape": "text",
    "style": "abstract",
    "text": "Hello World",
    "font": {
      "color-blue": 1.0,
      "color-green": 1.0,
      "color-red": 1.0,
      "size": 48.0,
      "tracking": 0.0,
      "name": "Arial",
      "weight": "Bold"
    },
    "horizontal-alignment": "center",
    "vertical-alignment": "center",
    "word-wrap": 1.0,
    "width": 400.0,
    "height": 100.0
  }
}
```

#### Callout Shapes
- `"shape-rectangle"`: Rectangle
- `"shape-rounded-rectangle"`: Rounded rectangle
- `"shape-ellipse"`: Ellipse/circle
- `"shape-triangle"`: Triangle
- `"shape-pentagon"`: Pentagon
- `"shape-hexagon"`: Hexagon
- `"shape-cloud"`: Cloud shape
- `"text"`: Text only

#### Text Attributes
```json
"textAttributes": {
  "type": "textAttributeList",
  "keyframes": [{
    "time": 0,
    "value": [
      {
        "name": "fontSize",
        "rangeStart": 0,
        "rangeEnd": 12,
        "value": 48.0,
        "valueType": "double"
      }
    ]
  }]
}
```

### Group
```json
{
  "_type": "Group",
  "medias": [
    // Array of nested media items
  ],
  "parameters": {
    // Group-level transformations
  }
}
```

## Media Parameters

### Transform Parameters
All visual media supports these transform parameters:

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `translation0` | X position | 0.0 | -∞ to +∞ |
| `translation1` | Y position | 0.0 | -∞ to +∞ |
| `scale0` | X scale | 1.0 | 0.0 to +∞ |
| `scale1` | Y scale | 1.0 | 0.0 to +∞ |
| `rotation0` | X rotation | 0.0 | -360 to 360 |
| `rotation1` | Y rotation | 0.0 | -360 to 360 |
| `rotation2` | Z rotation | 0.0 | -360 to 360 |
| `opacity` | Transparency | 1.0 | 0.0 to 1.0 |

### Cropping Parameters
| Parameter | Description | Default |
|-----------|-------------|---------|
| `geometryCrop0` | Left crop | 0.0 |
| `geometryCrop1` | Top crop | 0.0 |
| `geometryCrop2` | Right crop | 0.0 |
| `geometryCrop3` | Bottom crop | 0.0 |

## Media Metadata

Common metadata properties:

```json
"metadata": {
  "clipSpeedAttribute": false,
  "effectApplied": "none",
  "audiateLinkedSession": "",
  "mediaType": "video"
}
```

## Asset Properties

For grouped visual elements:

```json
"attributes": {
  "assetProperties": [{
    "type": 1,
    "name": "Callout",
    "objects": [41],  // IDs of grouped objects
    "themeMappings": {
      "fill": "background-1"
    }
  }]
}
```

## Best Practices

1. **Type Selection**
   - Use appropriate media type for content
   - Prefer UnifiedMedia for synchronized A/V
   - Use Groups for complex annotations

2. **Parameter Defaults**
   - Always include default transform values
   - Set opacity to 1.0 unless fading
   - Initialize scale to 1.0

3. **ID Management**
   - Ensure unique IDs across timeline
   - Use sequential numbering
   - Never reuse IDs

4. **Source References**
   - Verify source exists in sourceBin
   - Match trackNumber to available tracks
   - Handle missing sources gracefully