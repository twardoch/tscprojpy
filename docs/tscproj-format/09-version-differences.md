# Version Differences and Compatibility

Camtasia's `.tscproj` format has evolved over different versions. This document details the key differences and compatibility considerations.

## Version Identification

The version is identified by two key properties:

```json
{
  "version": "9.0",        // Format version
  "editRate": 705600000,   // Time precision indicator
  "authoringClientName": {
    "name": "Camtasia",
    "platform": "Mac",
    "version": "2025.1.4"  // Application version
  }
}
```

## Major Format Versions

### Version 4.0 (Legacy)
- **Camtasia versions**: 2020 and earlier
- **Edit rate**: 60
- **Time units**: Simple ticks (60 per second)
- **Features**: Basic editing capabilities

### Version 9.0 (Current)
- **Camtasia versions**: 2021 and later
- **Edit rate**: 705600000
- **Time units**: High-precision units
- **Features**: Advanced editing, sub-frame precision

## Key Differences

### 1. Time Representation

#### Version 4.0
```json
{
  "editRate": 60,
  "start": 120,      // 2 seconds (120 / 60)
  "duration": 300    // 5 seconds (300 / 60)
}
```

#### Version 9.0
```json
{
  "editRate": 705600000,
  "start": 1411200000,     // 2 seconds
  "duration": 3528000000   // 5 seconds
}
```

**Conversion formula**:
```
v9_time = v4_time * (705600000 / 60)
v4_time = v9_time * (60 / 705600000)
```

### 2. Property Additions

#### New in Version 9.0
```json
{
  "allowSubFrameEditing": false,
  "targetLoudness": -18.0,
  "shouldApplyLoudnessNormalization": true
}
```

These properties are:
- Not present in v4.0 files
- Have sensible defaults if missing
- Should be preserved when present

### 3. Media Structure Changes

#### Version 4.0 Source Tracks
```json
"sourceTracks": [
  {
    "range": [0, 10000],
    "type": 0,
    "editRate": 30,
    "sampleRate": 30,      // Simple number
    "metaData": ""         // Often empty
  }
]
```

#### Version 9.0 Source Tracks
```json
"sourceTracks": [
  {
    "range": [0, 10000],
    "type": 0,
    "editRate": 1000,
    "sampleRate": "2997/100",  // Precise fraction
    "metaData": "filename.mp4;",
    "parameters": {}           // New field
  }
]
```

### 4. Sample Rate Representation

#### Version 4.0
- Integer or float: `30`, `29.97`
- Less precise for fractional rates

#### Version 9.0
- String fractions: `"2997/100"`, `"12081/200"`
- Exact representation of fractional rates

### 5. Animation Differences

#### Version 4.0
```json
"scale0": {
  "type": "double",
  "keyframes": [
    {
      "time": 0,
      "value": 1.0,
      "interp": "linr"
      // No endTime or duration
    }
  ]
}
```

#### Version 9.0
```json
"scale0": {
  "type": "double",
  "defaultValue": 1.0,    // Added default
  "keyframes": [
    {
      "time": 0,
      "endTime": 58800000,
      "value": 1.0,
      "interp": "linr",
      "duration": 58800000  // Explicit duration
    }
  ]
}
```

### 6. Effect Enhancements

#### Version 4.0
- Basic effects set
- Limited parameters
- No effect IDs

#### Version 9.0
- Extended effect library
- Effect IDs for referencing
- More parameter options
- Support for custom effects

### 7. Transition Improvements

#### Version 4.0
```json
{
  "name": "Fade",
  "duration": 60,
  "rightMedia": 5
}
```

#### Version 9.0
```json
{
  "name": "Fade",
  "duration": 70560000,
  "rightMedia": 5,
  "attributes": {
    "bypass": false,
    "reverse": false,
    "trivial": false,
    "useAudioPreRoll": true,
    "useVisualPreRoll": true
  }
}
```

## Compatibility Guidelines

### Reading Files

When reading `.tscproj` files:

1. **Check version first**
   ```javascript
   if (data.version === "4.0") {
     // Use v4.0 parsing logic
   } else if (data.version === "9.0") {
     // Use v9.0 parsing logic
   }
   ```

2. **Handle missing properties**
   ```javascript
   const allowSubFrame = data.allowSubFrameEditing ?? false;
   const loudness = data.targetLoudness ?? -18.0;
   ```

3. **Parse sample rates**
   ```javascript
   function parseSampleRate(rate) {
     if (typeof rate === 'string' && rate.includes('/')) {
       const [num, den] = rate.split('/');
       return parseFloat(num) / parseFloat(den);
     }
     return parseFloat(rate);
   }
   ```

### Writing Files

When creating or modifying files:

1. **Maintain version consistency**
   - Don't mix v4.0 and v9.0 properties
   - Use appropriate editRate for version

2. **Time value conversion**
   ```javascript
   function convertTime(time, fromRate, toRate) {
     return Math.round(time * (toRate / fromRate));
   }
   ```

3. **Preserve unknown properties**
   - Keep properties you don't understand
   - Maintains forward compatibility

### Upgrading Projects

To upgrade v4.0 to v9.0:

1. **Update version and editRate**
   ```json
   "version": "9.0",
   "editRate": 705600000
   ```

2. **Convert all time values**
   ```javascript
   const ratio = 705600000 / 60;
   newTime = Math.round(oldTime * ratio);
   ```

3. **Add new properties**
   ```json
   "allowSubFrameEditing": false,
   "targetLoudness": -18.0,
   "shouldApplyLoudnessNormalization": true
   ```

4. **Update sample rate format**
   ```javascript
   // Convert 29.97 to "2997/100"
   function toFraction(decimal, precision = 100) {
     const numerator = Math.round(decimal * precision);
     return `${numerator}/${precision}`;
   }
   ```

## Platform Differences

### Mac vs Windows
```json
"authoringClientName": {
  "platform": "Mac" | "Windows"
}
```

Generally no format differences, but:
- File paths use forward slashes on both
- Media codec support may vary
- Some effects platform-specific

## Feature Support Matrix

| Feature | v4.0 | v9.0 |
|---------|------|------|
| Basic editing | ✓ | ✓ |
| Keyframe animation | ✓ | ✓ |
| Sub-frame editing | ✗ | ✓ |
| Loudness normalization | ✗ | ✓ |
| Fractional frame rates | Limited | ✓ |
| Advanced effects | Limited | ✓ |
| Custom effects | ✗ | ✓ |
| Effect IDs | ✗ | ✓ |
| Transition attributes | Basic | Full |

## Best Practices

1. **Version Detection**
   - Always check version before processing
   - Support both versions when possible
   - Fail gracefully for unknown versions

2. **Time Handling**
   - Use high precision math
   - Round appropriately
   - Test edge cases

3. **Property Management**
   - Provide defaults for missing properties
   - Preserve unknown properties
   - Validate property types

4. **Testing**
   - Test with files from different Camtasia versions
   - Verify time conversions
   - Check effect compatibility