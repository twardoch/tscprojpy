# Timeline Structure

The timeline is where all editing decisions are stored. It organizes media clips, effects, and transitions into a hierarchical structure of scenes and tracks.

## Timeline Root Structure

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

## Timeline Properties

### `id` (integer)
- **Description**: Unique identifier for the timeline
- **Required**: Yes
- **Example**: `22`

### `sceneTrack` (object)
- **Description**: Container for all scenes in the project
- **Required**: Yes
- **Contains**: `scenes` array

## Scene Structure

### `scenes` (array)
- **Description**: Array of scene objects
- **Note**: Most projects use a single scene
- **Structure**: Each scene contains a `csml` object

### `csml` (object)
- **Description**: Contains the actual track data
- **Required**: Yes
- **Properties**:
  - `tracks`: Array of track objects

## Track Structure

Tracks are layers in the timeline, rendered from bottom to top (lower indices are behind higher indices).

```json
{
  "trackIndex": 0,
  "medias": [...],
  "transitions": [...],
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

## Track Properties

### `trackIndex` (integer)
- **Description**: Track layer index (0 = bottom)
- **Required**: Yes
- **Note**: Lower indices render behind higher indices

### `medias` (array)
- **Description**: Array of media items on this track
- **Required**: Yes
- **See**: @05-media-types.md for media item structure

### `transitions` (array)
- **Description**: Array of transitions between clips
- **Default**: Empty array `[]`
- **See**: @07-effects-transitions.md for transition structure

### `parameters` (object)
- **Description**: Track-level parameters
- **Default**: Empty object `{}`
- **Common properties**:
  - Volume adjustments
  - Track effects

### `ident` (string)
- **Description**: Track identifier/name
- **Default**: Empty string `""`
- **Example**: `"Narration"`, `"Background Music"`

### `audioMuted` (boolean)
- **Description**: Whether audio is muted for this track
- **Default**: `false`

### `videoHidden` (boolean)
- **Description**: Whether video is hidden for this track
- **Default**: `false`

### `magnetic` (boolean)
- **Description**: Whether track has magnetic snapping enabled
- **Default**: `false`
- **Purpose**: Helps with clip alignment

### `matte` (integer)
- **Description**: Matte/mask mode
- **Default**: `0`
- **Values**:
  - `0`: No matte
  - Other values: Various matte modes

### `solo` (boolean)
- **Description**: Whether track is in solo mode
- **Default**: `false`
- **Purpose**: Isolates track for preview

### `metadata` (object)
- **Description**: Additional track metadata
- **Common properties**:
  - `IsLocked` (string): "True" or "False"
  - `trackHeight` (string): Visual height in pixels

## Track Organization

### Track Types by Convention

1. **Track 0-2**: Often used for primary content
   - Track 0: Background/base layer
   - Track 1: Main video content
   - Track 2: Overlays

2. **Audio Tracks**: Can be on any track index
   - Background music
   - Narration
   - Sound effects

3. **Annotation Tracks**: Higher indices
   - Callouts
   - Text overlays
   - Graphics

### Example Multi-Track Timeline

```json
"tracks": [
  {
    "trackIndex": 0,
    "ident": "Background",
    "medias": [/* background video/image */]
  },
  {
    "trackIndex": 1,
    "ident": "Main Content",
    "medias": [/* primary video clips */]
  },
  {
    "trackIndex": 2,
    "ident": "Music",
    "medias": [/* audio files */]
  },
  {
    "trackIndex": 3,
    "ident": "Annotations",
    "medias": [/* callouts and text */]
  }
]
```

## Media Placement

Media items on tracks have timing properties that determine their position:

```json
{
  "id": 25,
  "_type": "VMFile",
  "start": 164640000,      // Timeline position
  "duration": 1081920000,  // Display duration
  "mediaStart": 4727520000,  // In point in source
  "mediaDuration": 1081920000  // Used portion of source
}
```

### Timing Properties
- **`start`**: Position on timeline (in edit rate units)
- **`duration`**: How long it appears on timeline
- **`mediaStart`**: Start point within source media
- **`mediaDuration`**: Duration from source used

## Track Rendering Order

1. **Bottom to Top**: Lower `trackIndex` renders first
2. **Left to Right**: Earlier `start` times play first
3. **Transitions**: Applied between adjacent clips
4. **Effects**: Applied to individual clips or entire tracks

## Advanced Track Features

### Track Locking
```json
"metadata": {
  "IsLocked": "True"
}
```
Prevents accidental edits to track content.

### Track Height
```json
"metadata": {
  "trackHeight": "108"  // Double height
}
```
Visual representation in the editor.

### Solo Mode
```json
"solo": true
```
Isolates track for preview, muting all others.

### Magnetic Snapping
```json
"magnetic": true
```
Enables automatic alignment with other clips.

## Timeline Coordinates

All positions and timings use the project's coordinate system:
- **Time**: Based on project `editRate`
- **Position**: Canvas coordinates (0,0 = top-left)
- **Size**: In pixels relative to canvas

## Best Practices

1. **Track Organization**
   - Group related content on same track
   - Use meaningful track names (`ident`)
   - Keep consistent track heights

2. **Performance**
   - Limit number of simultaneous tracks
   - Avoid excessive track stacking
   - Use track hiding for performance

3. **Maintenance**
   - Preserve track metadata
   - Maintain track index continuity
   - Handle empty tracks gracefully

4. **Compatibility**
   - Support both locked and unlocked tracks
   - Handle missing transition references
   - Preserve unknown track properties