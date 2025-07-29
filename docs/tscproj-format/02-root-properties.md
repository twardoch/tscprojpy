# Root Level Properties

This document details all properties found at the root level of a `.tscproj` file. These properties define project-wide settings and metadata.

## Project Metadata

### `title` (string)
- **Description**: Project title
- **Default**: Empty string `""`
- **Example**: `"My Tutorial Video"`

### `description` (string)
- **Description**: Project description or notes
- **Default**: Empty string `""`
- **Example**: `"Introduction video for product launch"`

### `author` (string)
- **Description**: Project author/creator name
- **Default**: Empty string `""`
- **Example**: `"John Smith"`

## Canvas Dimensions

### `width` (float)
- **Description**: Canvas width in pixels
- **Required**: Yes
- **Common values**: `1920.0`, `1280.0`, `3840.0`
- **Example**: `1920.0`

### `height` (float)
- **Description**: Canvas height in pixels
- **Required**: Yes
- **Common values**: `1080.0`, `720.0`, `2160.0`
- **Example**: `1080.0`

## Video Settings

### `videoFormatFrameRate` (integer)
- **Description**: Target output frame rate
- **Common values**: `30`, `60`, `24`, `25`
- **Example**: `60`

### `allowSubFrameEditing` (boolean)
- **Description**: Enables sub-frame precision editing
- **Version**: 9.0+
- **Default**: `false`
- **Example**: `false`

## Audio Settings

### `audioFormatSampleRate` (integer)
- **Description**: Audio sample rate in Hz
- **Common values**: `44100`, `48000`
- **Example**: `44100`

### `targetLoudness` (float)
- **Description**: Target loudness in LUFS (Loudness Units relative to Full Scale)
- **Default**: `-18.0`
- **Range**: Typically -23.0 to -16.0
- **Example**: `-18.0`

### `shouldApplyLoudnessNormalization` (boolean)
- **Description**: Whether to apply loudness normalization to audio
- **Default**: `true`
- **Example**: `true`

## Version Information

### `version` (string)
- **Description**: Project format version
- **Values**: 
  - `"4.0"` - Camtasia 2020 and earlier
  - `"9.0"` - Camtasia 2021 and later
- **Required**: Yes
- **Example**: `"9.0"`

### `editRate` (integer)
- **Description**: Time base for all time values in the project
- **Values**:
  - `60` - Version 4.0 (60 ticks per second)
  - `705600000` - Version 9.0 (high precision)
- **Required**: Yes
- **Usage**: `seconds = timeValue / editRate`

### `authoringClientName` (object)
- **Description**: Information about the Camtasia version that created the file
- **Structure**:
  ```json
  {
    "name": "Camtasia",
    "platform": "Mac" | "Windows",
    "version": "2025.1.4"
  }
  ```

#### Sub-properties:
- `name` (string): Always "Camtasia"
- `platform` (string): Either "Mac" or "Windows"
- `version` (string): Camtasia version number

## Content Arrays

### `sourceBin` (array)
- **Description**: Array of all media sources used in the project
- **Required**: Yes
- **Structure**: Array of source media objects
- **See**: @03-source-media.md for detailed structure

### `timeline` (object)
- **Description**: The main timeline structure containing all edits
- **Required**: Yes
- **Structure**: Timeline object with scenes and tracks
- **See**: @04-timeline-structure.md for detailed structure

## Complete Example

```json
{
  "title": "Product Demo",
  "description": "Q1 2024 product demonstration video",
  "author": "Marketing Team",
  "targetLoudness": -18.0,
  "shouldApplyLoudnessNormalization": true,
  "videoFormatFrameRate": 60,
  "audioFormatSampleRate": 44100,
  "allowSubFrameEditing": false,
  "width": 1920.0,
  "height": 1080.0,
  "version": "9.0",
  "editRate": 705600000,
  "authoringClientName": {
    "name": "Camtasia",
    "platform": "Mac",
    "version": "2025.1.4"
  },
  "sourceBin": [...],
  "timeline": {...}
}
```

## Property Requirements by Version

### Version 4.0 Required Properties
- `width`, `height`
- `version`
- `editRate`
- `authoringClientName`
- `sourceBin`
- `timeline`

### Version 9.0 Additional Properties
- `allowSubFrameEditing`
- `targetLoudness`
- `shouldApplyLoudnessNormalization`

## Default Values

When creating new projects programmatically, use these defaults:

| Property | Default Value |
|----------|--------------|
| `title` | `""` |
| `description` | `""` |
| `author` | `""` |
| `targetLoudness` | `-18.0` |
| `shouldApplyLoudnessNormalization` | `true` |
| `videoFormatFrameRate` | `30` or `60` |
| `audioFormatSampleRate` | `44100` |
| `allowSubFrameEditing` | `false` |

## Validation Rules

1. **Dimensions**: Both `width` and `height` must be positive numbers
2. **Frame Rate**: Must be a standard video frame rate
3. **Sample Rate**: Must be a standard audio sample rate
4. **Version**: Must match the `editRate` value
5. **Edit Rate**: 
   - Version 4.0: Must be `60`
   - Version 9.0: Must be `705600000`