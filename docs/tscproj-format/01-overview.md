# Camtasia .tscproj Format Overview

## Purpose and Usage

The `.tscproj` file format is the native project format for TechSmith Camtasia, a professional screen recording and video editing software. These files store complete project information including:

- Media references (video, audio, images)
- Timeline arrangement and editing decisions
- Visual effects and transitions
- Annotations and callouts
- Project settings and metadata

## File Format

`.tscproj` files are stored as **JSON** (JavaScript Object Notation), making them:
- Human-readable when opened in a text editor
- Programmatically parseable and modifiable
- Version control friendly
- Cross-platform compatible

## JSON Structure Overview

The top-level structure follows this pattern:

```json
{
  // Project metadata and settings
  "title": "Project Title",
  "author": "Author Name",
  "description": "Project Description",
  
  // Canvas and format settings
  "width": 1920.0,
  "height": 1080.0,
  "videoFormatFrameRate": 60,
  "audioFormatSampleRate": 44100,
  
  // Version information
  "version": "9.0",
  "editRate": 705600000,
  "authoringClientName": {
    "name": "Camtasia",
    "platform": "Mac",
    "version": "2025.1.4"
  },
  
  // Media sources
  "sourceBin": [...],
  
  // Timeline structure
  "timeline": {...}
}
```

## Main Components

### 1. Root Properties
The root level contains project-wide settings:
- Canvas dimensions (width, height)
- Frame rate and audio settings
- Version and compatibility information
- Audio normalization settings

### 2. Source Bin (`sourceBin`)
An array containing all imported media files:
- Each item has a unique ID
- References to actual media files (relative paths)
- Source metadata (dimensions, duration, tracks)
- Import timestamps

### 3. Timeline (`timeline`)
The editing timeline structure:
- Scene-based organization
- Multiple tracks (layers)
- Media clips with timing information
- Effects and transitions

## File References

Media files are referenced using **relative paths** from the project file location:

```json
"src": "./media/1752976336.728338/video.mp4"
```

The typical structure:
- `./media/` - Standard media folder
- `{timestamp}/` - Unique folder per import session
- `{filename}` - Original or processed media file

## Coordinate System

Camtasia uses a standard 2D coordinate system:
- Origin (0,0) at top-left
- X increases rightward
- Y increases downward
- All measurements in pixels

## Time Representation

Time values vary by version:
- **Version 4.0**: Simple tick system (60 ticks/second)
- **Version 9.0**: High-precision units based on `editRate`

To convert to seconds:
```
seconds = timeValue / editRate
```

## Common Use Cases

### 1. Project Scaling
Modify canvas dimensions and scale all content:
- Update root `width` and `height`
- Scale all `rect` arrays
- Adjust position and scale parameters
- Update keyframe values

### 2. Media Management
- Replace file paths when moving projects
- Update source references
- Manage missing media

### 3. Batch Processing
- Automate repetitive edits
- Apply consistent settings across projects
- Generate projects programmatically

### 4. Analysis and Reporting
- Extract project statistics
- Audit media usage
- Generate edit decision lists (EDL)

## File Size Considerations

`.tscproj` files are typically small (KB to MB range) as they only contain:
- References to media (not the media itself)
- Editing metadata
- Effects parameters

The actual media files are stored separately in the media folder.

## Best Practices

1. **Backup Strategy**
   - Keep `.tscproj` files with their media folders
   - Use relative paths for portability
   - Version control the `.tscproj` files

2. **Compatibility**
   - Check version before processing
   - Handle both v4.0 and v9.0 formats
   - Preserve unknown properties for forward compatibility

3. **Validation**
   - Verify media file existence
   - Check dimension consistency
   - Validate time values

## Error Handling

Common issues when working with `.tscproj` files:
- Missing media files (broken references)
- Version incompatibilities
- Invalid JSON syntax
- Inconsistent dimensions or time values

Always validate the JSON structure and check media availability before processing.