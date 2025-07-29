# Effects and Transitions

Effects and transitions enhance media items with visual and audio processing. Effects apply to individual clips, while transitions blend between adjacent clips.

## Effects Structure

Effects are stored in the `effects` array of media items:

```json
"effects": [
  {
    "name": "ColorAdjustment",
    "effectId": 45,
    "enabled": true,
    "parameters": {
      "brightness": 0.1,
      "contrast": 1.2,
      "saturation": 0.8
    }
  }
]
```

## Effect Properties

### `name` (string)
- **Description**: Effect type identifier
- **Required**: Yes
- **Examples**: `"ColorAdjustment"`, `"Blur"`, `"DeviceShadow"`

### `effectId` (integer)
- **Description**: Unique ID for this effect instance
- **Required**: No
- **Note**: Used for effect references

### `enabled` (boolean)
- **Description**: Whether effect is active
- **Default**: `true`

### `parameters` (object)
- **Description**: Effect-specific parameters
- **Required**: Yes
- **Content**: Varies by effect type

## Common Effects

### Color Adjustment
```json
{
  "name": "ColorAdjustment",
  "parameters": {
    "brightness": 0.0,      // -1.0 to 1.0
    "contrast": 1.0,        // 0.0 to 2.0
    "saturation": 1.0,      // 0.0 to 2.0
    "gamma": 1.0,           // 0.1 to 3.0
    "hue": 0.0,             // -180 to 180
    "temperature": 0.0      // -100 to 100
  }
}
```

### Blur
```json
{
  "name": "Blur",
  "parameters": {
    "amount": 5.0,          // 0.0 to 100.0
    "type": "gaussian"      // "gaussian", "motion", "zoom"
  }
}
```

### Drop Shadow
```json
{
  "name": "DropShadow",
  "parameters": {
    "offsetX": 5.0,
    "offsetY": 5.0,
    "blur": 3.0,
    "opacity": 0.5,
    "color": {
      "red": 0.0,
      "green": 0.0,
      "blue": 0.0
    }
  }
}
```

### Device Frame
```json
{
  "name": "DeviceFrame",
  "parameters": {
    "device": "iPhone13",
    "orientation": "portrait",
    "scale": 1.0
  }
}
```

## Transitions Structure

Transitions are stored in the `transitions` array at the track level:

```json
"transitions": [
  {
    "name": "Glitch",
    "duration": 294000000,
    "rightMedia": 36,
    "attributes": {
      "Random": 0.0,
      "bypass": false,
      "reverse": false,
      "trivial": false,
      "useAudioPreRoll": true,
      "useVisualPreRoll": true
    }
  }
]
```

## Transition Properties

### `name` (string)
- **Description**: Transition type
- **Required**: Yes
- **Examples**: `"Fade"`, `"Glitch"`, `"Wipe"`, `"Slide"`

### `duration` (integer)
- **Description**: Transition length
- **Units**: Project edit rate units
- **Required**: Yes

### `rightMedia` (integer)
- **Description**: ID of the clip after the transition
- **Required**: Yes
- **Note**: Transition occurs between this and previous clip

### `attributes` (object)
- **Description**: Transition-specific parameters
- **Required**: Yes

## Common Transition Attributes

### Universal Attributes
```json
{
  "bypass": false,           // Skip transition
  "reverse": false,          // Reverse direction
  "trivial": false,          // Simple transition
  "useAudioPreRoll": true,   // Include audio fade
  "useVisualPreRoll": true   // Include visual fade
}
```

### Transition-Specific Attributes

#### Fade
```json
{
  "name": "Fade",
  "attributes": {
    "fadeColor": {
      "red": 0.0,
      "green": 0.0,
      "blue": 0.0
    }
  }
}
```

#### Wipe
```json
{
  "name": "Wipe",
  "attributes": {
    "direction": "left",     // "left", "right", "up", "down"
    "softness": 0.1
  }
}
```

#### Slide
```json
{
  "name": "Slide",
  "attributes": {
    "direction": "left",
    "overlap": true
  }
}
```

#### Glitch
```json
{
  "name": "Glitch",
  "attributes": {
    "Random": 0.0,          // Randomization amount
    "intensity": 0.5        // Effect intensity
  }
}
```

## Effect Chains

Multiple effects can be applied in sequence:

```json
"effects": [
  {
    "name": "ColorCorrection",
    "parameters": {...}
  },
  {
    "name": "Blur",
    "parameters": {...}
  },
  {
    "name": "Vignette",
    "parameters": {...}
  }
]
```

## Animated Effect Parameters

Effect parameters can be animated using keyframes:

```json
{
  "name": "Blur",
  "parameters": {
    "amount": {
      "type": "double",
      "defaultValue": 0.0,
      "keyframes": [
        {
          "time": 0,
          "value": 0.0,
          "interp": "linr"
        },
        {
          "time": 1000000,
          "value": 20.0,
          "interp": "linr"
        }
      ]
    }
  }
}
```

## Audio Effects

### Volume/Gain
```json
{
  "name": "AudioGain",
  "parameters": {
    "gain": 2.0,            // Multiplier
    "normalize": true
  }
}
```

### Noise Removal
```json
{
  "name": "NoiseRemoval",
  "parameters": {
    "sensitivity": 0.5,
    "amount": 0.8
  }
}
```

### Equalizer
```json
{
  "name": "Equalizer",
  "parameters": {
    "bass": 0.0,           // -12 to 12 dB
    "mid": 0.0,
    "treble": 0.0
  }
}
```

## Visual Effects

### Chroma Key (Green Screen)
```json
{
  "name": "ChromaKey",
  "parameters": {
    "keyColor": {
      "red": 0.0,
      "green": 1.0,
      "blue": 0.0
    },
    "tolerance": 0.1,
    "softness": 0.05,
    "spill": 0.2
  }
}
```

### Cursor Effects
```json
{
  "name": "CursorEffects",
  "parameters": {
    "highlight": true,
    "highlightColor": {...},
    "clickEffect": "ripple",
    "clickSound": true
  }
}
```

## Transition Placement

Transitions connect adjacent media items:

```
[Media A] -> [Transition] -> [Media B]
           ^                ^
           |                |
        End of A      rightMedia ID
```

### Duration Overlap
- Transition duration overlaps both clips
- Reduces effective duration of both clips
- Must not exceed either clip's duration

## Best Practices

1. **Effect Order**
   - Apply color correction first
   - Add stylistic effects next
   - Apply output effects last

2. **Performance**
   - Limit effect count per clip
   - Disable unused effects
   - Use simple transitions for better playback

3. **Transitions**
   - Keep transitions short (0.5-2 seconds)
   - Match transition style to content
   - Use consistent transitions throughout

4. **Parameter Ranges**
   - Stay within documented ranges
   - Test extreme values carefully
   - Provide defaults for all parameters

## Custom Effects

Some effects support custom parameters:

```json
{
  "name": "CustomEffect",
  "pluginId": "com.example.effect",
  "parameters": {
    "custom1": "value",
    "custom2": 123,
    "custom3": true
  }
}
```

## Version Compatibility

- Basic effects (Fade, Cut) supported in all versions
- Advanced effects may require specific Camtasia versions
- Unknown effects should be preserved but marked as unsupported