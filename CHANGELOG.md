# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2025-01-29

### Improved
- Enhanced version support with better error messages for legacy formats
- Added support for detecting Camtasia 2018 (v2.0) and 2019 (v3.0) versions
- Improved project structure validation with more graceful handling of missing fields
- Better error handling for invalid or malformed project files
- Added validation warnings when loading unsupported versions

### Fixed
- Fixed test for validate_structure to match new validation logic
- Updated linting and formatting issues

## [1.0.0] - 2025-01-29

### 🎉 First Major Release

### Added
- Initial implementation of `xyscale` command to scale Camtasia .tscproj files
- New `timescale` command for temporal scaling with audio duration preservation
- Complete architectural refactor with domain-driven design:
  - Domain models layer (`models/`) with immutable data structures
  - Serialization layer (`serialization/`) with version detection
  - Transform engine (`transforms/`) for applying transformations
- Media type support for UnifiedMedia, Group, and StitchedMedia
- Comprehensive test suite (`test_comprehensive.sh`)
- Project version detection and compatibility warnings
- Auto-generated output filenames when not specified
- Verbose logging mode with loguru for debugging
- Progress indicators using Rich library
- Comprehensive error handling and validation
- Comprehensive documentation of the .tscproj file format in `docs/tscproj-format.md`
- Updated README with professional documentation and usage examples

### Technical Details
- **xyscale** - Scales spatial properties:
  - Canvas width and height
  - Object positions (translation0, translation1, translation2)
  - Object scales (scale0, scale1, scale2)
  - Geometry crop values
  - Rectangle arrays (rect, trackRect)
  - Callout definition properties (width, height, corner-radius, stroke-width)
  - Default dimension metadata
  - Keyframe animation values for spatial properties

- **timescale** - Scales temporal properties:
  - Timeline duration and media timing
  - Media start times and durations
  - Keyframe timing for animations
  - Transition durations
  - **Preserves audio duration** - audio clips maintain their length but are repositioned

### Architecture
- Domain models: Canvas, Project, Media hierarchy, Timeline, SourceBin
- Transform engine with PropertyTransformer for spatial and temporal transforms
- Serialization with ProjectLoader and ProjectSaver
- Version detection supporting Camtasia 2020 (v4.0) and 2021+ (v9.0)
- Media factory for proper deserialization of different media types

### Documentation
- Created detailed .tscproj file format specification
- Analyzed over 200 example files to understand format variations
- Documented all media types, timeline structure, and version differences
- Added comprehensive usage examples in README
- Documented architecture and maintenance guidelines

### Improved
- Refactored existing scaler.py to use new domain model architecture
- Better separation of concerns with layered architecture
- More robust media type handling
- Cleaner CLI implementation using the new components

## [0.1.0] - Initial Release
- Project skeleton with Fire CLI and Rich output
- Basic project structure with hatch-vcs versioning