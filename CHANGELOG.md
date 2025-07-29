# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial implementation of `xyscale` command to scale Camtasia .tscproj files
- Core scaling functionality in `scaler.py` module
- Support for scaling canvas dimensions, object positions, and sizes
- Intelligent scaling of different property types (dimensions, scales, positions)
- Support for scaling keyframe animation values
- Auto-generated output filenames when not specified
- Verbose logging mode for debugging
- Progress indicators using Rich library
- Comprehensive error handling and validation
- Comprehensive documentation of the .tscproj file format in `docs/tscproj-format.md`
- Updated README with professional documentation and usage examples

### Technical Details
- Scales the following properties:
  - Canvas width and height
  - Object positions (translation0, translation1, translation2)
  - Object scales (scale0, scale1, scale2)
  - Geometry crop values
  - Rectangle arrays (rect, trackRect)
  - Callout definition properties (width, height, corner-radius, stroke-width)
  - Default dimension metadata
  - Keyframe animation values

### Documentation
- Created detailed .tscproj file format specification
- Analyzed over 200 example files to understand format variations
- Documented all media types, timeline structure, and version differences
- Added comprehensive usage examples in README

### Planning
- Created detailed plans for version support enhancement
- Designed timescale operation for changing playback speed
- Planned audio handling strategy (preserve duration, reposition only)
- Documented implementation phases and technical considerations

## [0.1.0] - Initial Release
- Project skeleton with Fire CLI and Rich output
- Basic project structure with hatch-vcs versioning