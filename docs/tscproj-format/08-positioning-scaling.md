# Coordinate Systems and Transformations

This document explains how positioning, scaling, and transformations work in Camtasia projects, essential for correctly manipulating content.

## Coordinate System

Camtasia uses a standard 2D coordinate system:

```
(0,0) ────────────► X (width)
  │
  │
  │
  ▼
  Y (height)
```

- **Origin**: Top-left corner (0, 0)
- **X-axis**: Increases rightward
- **Y-axis**: Increases downward
- **Units**: Pixels

## Canvas vs. Media Coordinates

### Canvas Space
- Defined by root `width` and `height`
- All visible content rendered within
- Media can extend beyond canvas (cropped)

### Media Space
- Each media item has its own coordinate space
- Transformations applied relative to media center
- Original dimensions preserved in `sourceBin`

## Rectangle Arrays

Rectangle arrays define bounding boxes throughout the format:

```json
"rect": [x, y, width, height]
```

### Usage Locations
1. **sourceBin**: Original media dimensions
   ```json
   "rect": [0, 0, 1920, 1080]  // Full HD video
   ```

2. **trackRect**: Track-specific dimensions
   ```json
   "trackRect": [0, 0, 1920, 1080]  // Video track
   "trackRect": [0, 0, 0, 0]        // Audio track
   ```

3. **Callout dimensions**: Size before transforms
   ```json
   "width": 240.0,
   "height": 180.0
   ```

## Transformation Parameters

All visual media supports these transformation parameters:

### Translation (Position)
```json
"parameters": {
  "translation0": 100.0,    // X offset from center
  "translation1": -50.0     // Y offset from center
}
```

- **Reference point**: Canvas center
- **Default**: (0.0, 0.0) = centered on canvas
- **Calculation**: 
  ```
  finalX = (canvasWidth / 2) + translation0
  finalY = (canvasHeight / 2) + translation1
  ```

### Scale
```json
"parameters": {
  "scale0": 1.5,    // X scale factor
  "scale1": 1.5     // Y scale factor
}
```

- **Reference point**: Media center
- **Default**: 1.0 = original size
- **Range**: 0.0 to ∞ (practical limit ~10.0)

### Rotation
```json
"parameters": {
  "rotation0": 0.0,    // X-axis rotation (3D tilt)
  "rotation1": 0.0,    // Y-axis rotation (3D tilt)
  "rotation2": 45.0    // Z-axis rotation (2D spin)
}
```

- **Units**: Degrees
- **Range**: -360 to 360 (wraps around)
- **Most common**: `rotation2` for 2D rotation

### Opacity
```json
"parameters": {
  "opacity": 0.75    // 75% visible
}
```

- **Range**: 0.0 (transparent) to 1.0 (opaque)
- **Default**: 1.0

## Geometry Cropping

Crop edges of media without affecting position:

```json
"parameters": {
  "geometryCrop0": 10.0,    // Crop 10px from left
  "geometryCrop1": 20.0,    // Crop 20px from top
  "geometryCrop2": 10.0,    // Crop 10px from right
  "geometryCrop3": 20.0     // Crop 20px from bottom
}
```

- **Units**: Pixels in source media space
- **Applied before**: Scale and rotation

## Transformation Order

Transformations are applied in this order:
1. **Crop** - Remove edges
2. **Scale** - Resize
3. **Rotation** - Rotate around center
4. **Translation** - Position on canvas

## Scaling Calculations

### Media to Canvas Fit

To fit media to canvas maintaining aspect ratio:

```javascript
// Source dimensions
const srcWidth = 1920;
const srcHeight = 1080;
const srcAspect = srcWidth / srcHeight;

// Target dimensions
const canvasWidth = 1280;
const canvasHeight = 720;
const canvasAspect = canvasWidth / canvasHeight;

// Calculate scale
let scale;
if (srcAspect > canvasAspect) {
  // Fit to width
  scale = canvasWidth / srcWidth;
} else {
  // Fit to height
  scale = canvasHeight / srcHeight;
}

// Apply uniform scale
scale0 = scale;
scale1 = scale;
```

### Project Scaling

When scaling entire project (e.g., 1080p to 4K):

```javascript
const scaleFactor = 2.0;  // 1920x1080 to 3840x2160

// Scale canvas
newWidth = oldWidth * scaleFactor;
newHeight = oldHeight * scaleFactor;

// Scale all rect arrays
newRect = oldRect.map(v => v * scaleFactor);

// Scale positions
newTranslation0 = oldTranslation0 * scaleFactor;
newTranslation1 = oldTranslation1 * scaleFactor;

// Scale sizes (for callouts)
newWidth = oldWidth * scaleFactor;
newHeight = oldHeight * scaleFactor;

// Scales remain the same!
// scale0 and scale1 are relative factors
```

## Callout Positioning

Callouts have additional positioning considerations:

```json
{
  "_type": "Callout",
  "def": {
    "width": 200.0,      // Base width
    "height": 100.0      // Base height
  },
  "parameters": {
    "translation0": 50.0,
    "translation1": -100.0,
    "scale0": 1.5,       // Final width = 200 * 1.5 = 300
    "scale1": 2.0        // Final height = 100 * 2.0 = 200
  }
}
```

## Multi-Resolution Support

### Source Material
```json
"sourceBin": [
  {
    "rect": [0, 0, 3840, 2160],  // 4K source
    "trackRect": [0, 0, 3840, 2160]
  }
]
```

### Canvas Output
```json
"width": 1920.0,   // HD output
"height": 1080.0
```

### Media Scaling
```json
"parameters": {
  "scale0": 0.5,    // Scale 4K to HD
  "scale1": 0.5
}
```

## Common Positioning Patterns

### Center on Canvas
```json
"translation0": 0.0,
"translation1": 0.0
```

### Top-Left Corner
```json
// For 1920x1080 canvas, 640x480 media
"translation0": -640.0,   // -(canvasWidth/2 - mediaWidth/2)
"translation1": -300.0    // -(canvasHeight/2 - mediaHeight/2)
```

### Picture-in-Picture
```json
// Small video in corner
"scale0": 0.25,
"scale1": 0.25,
"translation0": 600.0,    // Right side
"translation1": -300.0    // Top
```

## Anchor Point Calculations

Media items are positioned relative to their center:

```
centerX = x + (width * scale0) / 2
centerY = y + (height * scale1) / 2

// Position for translation (0,0)
x = (canvasWidth / 2) - (mediaWidth * scale0 / 2)
y = (canvasHeight / 2) - (mediaHeight * scale1 / 2)
```

## Best Practices

1. **Aspect Ratio Preservation**
   - Keep `scale0` and `scale1` equal
   - Use uniform scaling when resizing projects
   - Calculate scales based on aspect ratios

2. **Resolution Independence**
   - Store original dimensions in sourceBin
   - Use relative scales rather than absolute sizes
   - Design for multiple output resolutions

3. **Performance Optimization**
   - Avoid extreme scale values (>5.0 or <0.1)
   - Crop before scaling when possible
   - Use appropriate source resolution

4. **Precision**
   - Use floating-point for all values
   - Maintain precision during calculations
   - Round only for final pixel output

## Debugging Position Issues

To debug positioning:

1. Check canvas dimensions
2. Verify source media dimensions
3. Calculate expected position:
   ```
   expectedX = canvasWidth/2 + translation0
   expectedY = canvasHeight/2 + translation1
   ```
4. Account for scale factors
5. Check for crop values
6. Verify transformation order