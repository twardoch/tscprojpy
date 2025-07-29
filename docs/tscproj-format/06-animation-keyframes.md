# Animation and Keyframe System

Camtasia supports keyframe-based animation for many properties, allowing smooth transitions and movements over time.

## Animation Structure

Animated properties replace simple values with keyframe objects:

```json
// Static property
"scale0": 1.0

// Animated property
"scale0": {
  "type": "double",
  "defaultValue": 1.0,
  "keyframes": [...]
}
```

## Keyframe Object Structure

```json
{
  "type": "double",
  "defaultValue": 1.0,
  "keyframes": [
    {
      "time": 0,
      "endTime": 58800000,
      "value": 0.5,
      "interp": "linr",
      "duration": 58800000
    },
    {
      "time": 58800000,
      "endTime": 117600000,
      "value": 1.5,
      "interp": "linr",
      "duration": 58800000
    }
  ]
}
```

## Keyframe Properties

### `type` (string)
- **Description**: Data type of the animated property
- **Values**: `"double"`, `"int"`, `"color"`
- **Required**: Yes

### `defaultValue` (varies)
- **Description**: Default value when no keyframes apply
- **Type**: Matches the `type` field
- **Required**: Yes

### `keyframes` (array)
- **Description**: Array of keyframe objects
- **Required**: Yes
- **Note**: Must be in chronological order

## Individual Keyframe Properties

### `time` (integer)
- **Description**: Start time of this keyframe
- **Units**: Media item's local time (0 = start of clip)
- **Required**: Yes

### `endTime` (integer)
- **Description**: End time of this keyframe's influence
- **Units**: Media item's local time
- **Required**: Yes
- **Note**: Usually matches next keyframe's `time`

### `value` (varies)
- **Description**: Property value at this keyframe
- **Type**: Matches parent's `type`
- **Required**: Yes

### `interp` (string)
- **Description**: Interpolation method to next keyframe
- **Values**:
  - `"linr"`: Linear interpolation
  - `"step"`: Step/hold (no interpolation)
  - `"bezr"`: Bezier curve
- **Default**: `"linr"`

### `duration` (integer)
- **Description**: Duration to next keyframe
- **Units**: Same as `time`
- **Calculation**: `nextKeyframe.time - this.time`

## Animatable Properties

### Transform Properties
- `translation0`, `translation1` - X/Y position
- `scale0`, `scale1` - X/Y scale
- `rotation0`, `rotation1`, `rotation2` - X/Y/Z rotation
- `opacity` - Transparency

### Audio Properties
- `volume` - Audio level
- `gain` - Audio gain

### Callout Properties
- Color components (RGB values)
- Size dimensions
- Text properties

## Animation Examples

### Simple Fade In/Out
```json
"opacity": {
  "type": "double",
  "defaultValue": 1.0,
  "keyframes": [
    {
      "time": 0,
      "endTime": 1000000,
      "value": 0.0,
      "interp": "linr",
      "duration": 1000000
    },
    {
      "time": 1000000,
      "endTime": 5000000,
      "value": 1.0,
      "interp": "linr",
      "duration": 4000000
    },
    {
      "time": 5000000,
      "endTime": 6000000,
      "value": 0.0,
      "interp": "linr",
      "duration": 1000000
    }
  ]
}
```

### Scale Animation (Zoom Effect)
```json
"scale0": {
  "type": "double",
  "defaultValue": 1.0,
  "keyframes": [
    {
      "time": 0,
      "endTime": 2000000,
      "value": 1.0,
      "interp": "linr",
      "duration": 2000000
    },
    {
      "time": 2000000,
      "endTime": 4000000,
      "value": 1.5,
      "interp": "linr",
      "duration": 2000000
    }
  ]
}
```

### Position Animation (Movement)
```json
"translation0": {
  "type": "double",
  "defaultValue": 0.0,
  "keyframes": [
    {
      "time": 0,
      "endTime": 3000000,
      "value": -100.0,
      "interp": "bezr",
      "duration": 3000000
    },
    {
      "time": 3000000,
      "endTime": 6000000,
      "value": 100.0,
      "interp": "bezr",
      "duration": 3000000
    }
  ]
}
```

## Animation Tracks Container

Media items can have multiple animated properties:

```json
"animationTracks": {
  "scale0": {...},
  "scale1": {...},
  "translation0": {...},
  "translation1": {...},
  "opacity": {...}
}
```

## Text Animation

Text callouts support character-range animations:

```json
"textAttributes": {
  "type": "textAttributeList",
  "keyframes": [
    {
      "time": 0,
      "endTime": 0,
      "value": [
        {
          "name": "fontSize",
          "rangeStart": 0,
          "rangeEnd": 5,
          "value": 24.0,
          "valueType": "double"
        },
        {
          "name": "fontSize",
          "rangeStart": 5,
          "rangeEnd": 10,
          "value": 48.0,
          "valueType": "double"
        }
      ],
      "duration": 0
    }
  ]
}
```

### Text Attribute Properties
- `name`: Attribute name (fontSize, fontColor, etc.)
- `rangeStart`: Character index start
- `rangeEnd`: Character index end
- `value`: Attribute value
- `valueType`: Data type

## Time Calculations

### Converting Keyframe Time to Timeline Time
```
timelineTime = mediaStart + (keyframeTime * scalar)
```

### Converting to Seconds
```
seconds = time / editRate
```

## Interpolation Types

### Linear (`"linr"`)
- Constant rate of change
- Straight line between keyframes
- Most common type

### Step (`"step"`)
- No interpolation
- Instant change at keyframe
- Used for on/off states

### Bezier (`"bezr"`)
- Smooth curved interpolation
- Acceleration/deceleration
- Natural motion effects

## Best Practices

1. **Keyframe Organization**
   - Keep keyframes in chronological order
   - Ensure `endTime` matches next `time`
   - Set proper `duration` values

2. **Performance**
   - Minimize keyframe count
   - Use linear interpolation when possible
   - Group related animations

3. **Scaling Animations**
   - Scale keyframe values proportionally
   - Maintain aspect ratios for scale animations
   - Adjust position keyframes for new canvas size

4. **Validation**
   - Check time continuity
   - Verify value ranges
   - Ensure type consistency

## Common Animation Patterns

### Ken Burns Effect
```json
// Slow zoom and pan
"scale0": { /* gradual increase */ },
"scale1": { /* gradual increase */ },
"translation0": { /* slow pan */ },
"translation1": { /* slow pan */ }
```

### Bounce Effect
```json
// Multiple keyframes with overshoot
"translation1": {
  "keyframes": [
    {"value": 0},
    {"value": 100},
    {"value": 80},
    {"value": 100},
    {"value": 95},
    {"value": 100}
  ]
}
```

### Typewriter Effect
```json
// Progressive text reveal using opacity per character
"textAttributes": {
  // Animate opacity from 0 to 1 for each character
}
```