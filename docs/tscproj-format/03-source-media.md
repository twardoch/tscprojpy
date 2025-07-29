# Source Media Management

The `sourceBin` array contains all media files imported into the project. Each source item represents a unique media file with its metadata, tracks, and properties.

## sourceBin Structure

```json
"sourceBin": [
  {
    "id": 1,
    "src": "./media/1752976336.728338/video.mp4",
    "rect": [0, 0, 1920, 1080],
    "lastMod": "20250419T143221",
    "loudnessNormalization": true,
    "sourceTracks": [...],
    "metadata": {...}
  }
]
```

## Source Item Properties

### `id` (integer)
- **Description**: Unique identifier for this source
- **Required**: Yes
- **Usage**: Referenced by media items in the timeline
- **Example**: `1`, `2`, `3`

### `src` (string)
- **Description**: Relative path to the media file
- **Required**: Yes
- **Format**: `./media/{timestamp}/{filename}`
- **Example**: `"./media/1752976336.728338/intro.mp4"`

### `rect` (array[4])
- **Description**: Bounding rectangle of the media
- **Format**: `[x, y, width, height]`
- **Required**: Yes
- **Notes**: 
  - For video/images: actual dimensions
  - For audio: `[0, 0, 0, 0]`
- **Example**: `[0, 0, 1920, 1080]`

### `lastMod` (string)
- **Description**: Last modification timestamp of the source file
- **Format**: ISO 8601 basic format `YYYYMMDDTHHMMSS`
- **Example**: `"20250419T143221"`

### `loudnessNormalization` (boolean)
- **Description**: Whether loudness normalization is enabled
- **Default**: `true`
- **Applies to**: Audio tracks only

### `sourceTracks` (array)
- **Description**: Array of tracks within the source media
- **Required**: Yes
- **Notes**: A media file can contain multiple tracks (e.g., video + audio)

### `metadata` (object)
- **Description**: Additional metadata about the source
- **Common properties**:
  - `timeAdded`: Timestamp when media was imported
  - Other custom properties

## Source Tracks Structure

Each source can contain multiple tracks representing different streams:

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
    "metaData": "filename.mp4;",
    "parameters": {}
  }
]
```

## Track Properties

### `range` (array[2])
- **Description**: Start and end points of the track
- **Format**: `[start, end]`
- **Units**: Track-specific time units based on `editRate`
- **Example**: `[0, 9817]`

### `type` (integer)
- **Description**: Track type identifier
- **Values**:
  - `0`: Video track
  - `1`: Image/still track
  - `2`: Audio track
- **Required**: Yes

### `editRate` (integer)
- **Description**: Time base for this track
- **Common values**:
  - Video: `1000`, `600`, `30000`, `44100`
  - Audio: `44100`, `48000`
- **Usage**: Used to calculate actual duration

### `trackRect` (array[4])
- **Description**: Track dimensions
- **Format**: `[x, y, width, height]`
- **Notes**:
  - Video/Image: Actual dimensions
  - Audio: `[0, 0, 0, 0]`

### `sampleRate` (number/string)
- **Description**: Sample rate for the track
- **Format**: 
  - Number: Direct rate (e.g., `60`)
  - String fraction: Precise rate (e.g., `"2997/100"` for 29.97 fps)
- **Video**: Frame rate
- **Audio**: Audio sample rate

### `bitDepth` (integer)
- **Description**: Bit depth of the track
- **Note**: Often `0` for video tracks

### `numChannels` (integer)
- **Description**: Number of audio channels
- **Values**:
  - `0`: No audio (video/image tracks)
  - `1`: Mono
  - `2`: Stereo
  - Higher values for multi-channel audio

### `integratedLUFS` (float)
- **Description**: Integrated loudness in LUFS
- **Default**: `100.0` for non-audio tracks
- **Range**: Typically -40.0 to 0.0 for audio

### `peakLevel` (float)
- **Description**: Peak audio level
- **Default**: `-1.0` for non-audio tracks
- **Range**: 0.0 to 1.0 for audio (linear scale)

### `tag` (integer)
- **Description**: Additional track identifier/tag
- **Default**: `0`

### `metaData` (string)
- **Description**: Track metadata string
- **Format**: Often contains filename with semicolon separator
- **Example**: `"video.mp4;"`

### `parameters` (object)
- **Description**: Additional track parameters
- **Default**: Empty object `{}`

## Media File Organization

### Directory Structure
```
project.tscproj
media/
  ├── 1752976336.728338/
  │   ├── video1.mp4
  │   └── audio1.mp3
  └── 1752976336.729220/
      └── image1.png
```

### Timestamp Folders
- Format: Unix timestamp with microseconds
- Purpose: Avoid naming conflicts
- Created during import session

## Common Source Patterns

### Video with Audio
```json
{
  "id": 1,
  "src": "./media/1752976336.728338/video.mp4",
  "rect": [0, 0, 1920, 1080],
  "sourceTracks": [
    {
      "type": 0,  // Video track
      "trackRect": [0, 0, 1920, 1080],
      "numChannels": 0
    },
    {
      "type": 2,  // Audio track
      "trackRect": [0, 0, 0, 0],
      "numChannels": 2
    }
  ]
}
```

### Audio Only
```json
{
  "id": 2,
  "src": "./media/1752976336.729220/music.mp3",
  "rect": [0, 0, 0, 0],
  "sourceTracks": [
    {
      "type": 2,
      "numChannels": 2,
      "sampleRate": 44100
    }
  ]
}
```

### Still Image
```json
{
  "id": 3,
  "src": "./media/1752976336.730231/logo.png",
  "rect": [0, 0, 512, 512],
  "sourceTracks": [
    {
      "type": 1,
      "trackRect": [0, 0, 512, 512],
      "numChannels": 0
    }
  ]
}
```

## Duration Calculation

To calculate actual duration in seconds:

### For Version 4.0
```
durationSeconds = (range[1] - range[0]) / editRate
```

### For Version 9.0
```
// First convert track time to project time
projectTime = (range[1] - range[0]) * (projectEditRate / trackEditRate)
// Then to seconds
durationSeconds = projectTime / projectEditRate
```

## Best Practices

1. **Path Management**
   - Always use relative paths
   - Maintain media folder structure
   - Handle missing files gracefully

2. **ID Assignment**
   - Use sequential integers
   - Never reuse IDs
   - Start from 1

3. **Metadata Preservation**
   - Preserve unknown properties
   - Maintain timestamp formats
   - Keep original filenames in metaData

4. **Track Analysis**
   - Check `type` to determine track nature
   - Use `numChannels` to identify audio
   - Verify `trackRect` matches `rect` for video