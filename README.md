# tscprojpy

`tscprojpy` is a Python package for parsing and manipulating Camtasia `.tscproj` project files programmatically. It enables automated workflows for video project management, scaling, and transformation.

## Quick Start

### Installation

```bash
pip install tscprojpy
```

### Basic Usage

```bash
# Scale a project to 150%
tscprojpy xyscale --input project.tscproj --scale 150.0

# Scale to 4K with custom output
tscprojpy xyscale --input project.tscproj --scale 200.0 --output project_4k.tscproj
```

## Why tscprojpy?

### The Problem

Camtasia is a powerful screen recording and video editing tool, but it lacks programmatic access to project files. When you need to:
- Convert projects between different resolutions (1080p → 4K)
- Batch process multiple projects
- Integrate Camtasia into automated workflows
- Analyze project structure programmatically

You're stuck doing everything manually through the GUI.

### The Solution

`tscprojpy` treats Camtasia project files (.tscproj) as data, enabling:
- **Automated scaling**: Resize projects without manual adjustment
- **Batch operations**: Process multiple files programmatically  
- **Integration**: Build Camtasia into larger video production pipelines
- **Analysis**: Extract project metadata and structure

## How It Works

### Understanding .tscproj Files

Camtasia project files are JSON documents containing:
- **Canvas settings**: Resolution, frame rate
- **Media library**: All imported assets (sourceBin)
- **Timeline**: Tracks, clips, effects, and animations
- **Metadata**: Project info and settings

### The Scaling Process

When you scale a project:

1. **Canvas dimensions** are multiplied by the scale factor
2. **All positions** (x, y coordinates) are scaled proportionally
3. **All sizes** (width, height) are scaled to match
4. **Animations** maintain their relative positions
5. **Effects** preserve their visual relationships

This ensures your project looks identical at the new resolution.

## Detailed Usage

### Command Line Interface

#### xyscale - Spatial Scaling

Scales all spatial properties in a project:

```bash
# Basic scaling
tscprojpy xyscale --input project.tscproj --scale 150.0

# Options
--input PATH      Input .tscproj file (required)
--scale FLOAT     Scale percentage, e.g., 150.0 for 150% (required)
--output PATH     Output file (optional, auto-generated if omitted)
--verbose         Enable detailed logging
```

**What gets scaled:**
- Canvas width and height
- Object positions (translation0, translation1)
- Object sizes (scale0, scale1)
- Rectangle arrays (rect, trackRect)
- Crop values (geometryCrop0-3)
- Callout dimensions and styling
- Keyframe values for animations

**Auto-generated filenames:**
- `project.tscproj` → `project_150pct.tscproj`
- `video.tscproj` → `video_200pct.tscproj`

### Python API (Future)

```python
from tscprojpy import Project

# Load a project
project = Project.load("my_video.tscproj")

# Scale to 4K
project.scale(2.0)  # 200%

# Save
project.save("my_video_4k.tscproj")
```

## Technical Architecture

### Core Components

```
tscprojpy/
├── cli.py          # Command-line interface (Fire-based)
├── scaler.py       # Core scaling engine
├── __init__.py     # Package initialization
└── _version.py     # Version management (hatch-vcs)
```

### Scaling Engine Design

The `TscprojScaler` class uses a recursive traversal pattern:

```python
class TscprojScaler:
    # Property sets for different scaling rules
    SCALE_PROPERTIES = {'width', 'height', 'translation0', ...}
    MULTIPLY_SCALE_PROPERTIES = {'scale0', 'scale1', ...}
    DIMENSION_ARRAYS = {'rect', 'trackRect'}
```

**Key design decisions:**

1. **Recursive traversal**: Handles arbitrary nesting depth
2. **Property detection**: Uses sets for O(1) lookup performance
3. **Type-aware scaling**: Different rules for different property types
4. **Preservation**: Non-spatial properties remain untouched

### Property Scaling Rules

| Property Type | Scaling Rule | Example |
|--------------|--------------|---------|
| Dimensions | Direct multiplication | `width: 1920` → `width: 2880` (1.5x) |
| Positions | Direct multiplication | `translation0: 100` → `translation0: 150` |
| Scales | Multiplication | `scale0: 0.5` → `scale0: 0.75` |
| Arrays | Element-wise | `rect: [0,0,1920,1080]` → `rect: [0,0,2880,1620]` |
| Time values | No change | `start: 1000` → `start: 1000` |
| Colors/Opacity | No change | `opacity: 0.5` → `opacity: 0.5` |

### Version Compatibility

| Camtasia Version | .tscproj Version | Support Status |
|-----------------|------------------|----------------|
| 2020 and earlier | 4.0 | ✅ Full support |
| 2021-2025 | 9.0 | ✅ Full support |
| Future versions | Unknown | ⚠️ Best effort |

## Development Guide

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/tscprojpy.git
cd tscprojpy

# Install with development dependencies
pip install -e ".[dev]"

# Or use uv (recommended)
uv sync
```

### Project Structure

```
tscprojpy/
├── src/tscprojpy/      # Source code
├── tests/              # Test suite
├── docs/               # Documentation
│   └── tscproj-format.md  # File format specification
├── example/            # Sample .tscproj files
└── pyproject.toml      # Project configuration
```

### Code Style and Quality

```bash
# Run linter
python -m ruff check src/

# Format code
python -m ruff format src/

# Run tests
python -m pytest

# Type checking (future)
python -m mypy src/
```

### Testing Strategy

1. **Unit tests**: Test individual scaling functions
2. **Integration tests**: Test CLI commands end-to-end
3. **Property tests**: Verify scaling mathematics
4. **Regression tests**: Use example files to prevent breaks

### Adding New Operations

To add a new operation (e.g., `rotate`):

1. Create operation class inheriting from base:
```python
class ProjectRotator(TscprojScaler):
    def rotate_project(self, angle: float):
        # Implementation
```

2. Add CLI command:
```python
def rotate(input: str, angle: float, output: str = None):
    """Rotate all content by angle degrees."""
    # Implementation
```

3. Register in Fire CLI:
```python
fire.Fire({
    "xyscale": xyscale,
    "rotate": rotate,  # New command
})
```

### Debugging Tips

1. **Use verbose mode**: `--verbose` enables detailed logging
2. **Check JSON diff**: Compare input/output with a JSON diff tool
3. **Validate in Camtasia**: Always test output files in Camtasia
4. **Small test files**: Create minimal test cases for debugging

## Future Roadmap

### Planned Features

1. **Time scaling** (`timescale`): Change playback speed
2. **Project assembly**: Create .tscproj files from scratch
3. **Batch processing**: Process entire directories
4. **Analysis tools**: Extract project statistics
5. **Python API**: Direct programmatic access

### Architecture Evolution

```
Current:
CLI → Scaler → JSON → File

Future:
CLI ─┐
     ├→ Operations → Project Model → Serializer → File
API ─┘
```

## Maintenance Notes

### Version Management

- Uses `hatch-vcs` for version management
- Version derived from git tags
- Tag format: `v0.1.0`, `v1.0.0`

### Release Process

1. Update CHANGELOG.md
2. Create git tag: `git tag v0.2.0`
3. Build: `python -m build`
4. Upload: `python -m twine upload dist/*`

### Dependency Management

- Minimal dependencies for reliability
- Core: `fire` (CLI), `rich` (UI), `loguru` (logging)
- Development: `pytest`, `ruff`
- No heavy dependencies (numpy, pandas, etc.)

### Performance Considerations

- JSON parsing is the bottleneck for large files
- Recursive traversal is O(n) where n = total properties
- Memory usage is 2x file size (input + output)
- Consider streaming for very large projects (future)

## Troubleshooting

### Common Issues

**"Input file does not exist"**
- Check file path is correct
- Use absolute paths if relative paths fail

**"Scale factor must be positive"**
- Scale is a percentage: use 150.0 for 150%, not 1.5

**Output looks wrong in Camtasia**
- Ensure you're using a compatible Camtasia version
- Check if project has custom effects that need manual adjustment

**Large file performance**
- Use `--verbose` to see progress
- Consider breaking very large projects into smaller ones

## Contributing

We welcome contributions! See CONTRIBUTING.md for guidelines.

### Areas for Contribution

- Additional operations (crop, rotate, effects)
- Performance optimizations
- Test coverage improvements
- Documentation and examples
- Bug fixes and edge cases

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- Inspired by the need for automated video production workflows
- Thanks to the Camtasia community for file format insights
- Built with modern Python tooling (Fire, Rich, Ruff)