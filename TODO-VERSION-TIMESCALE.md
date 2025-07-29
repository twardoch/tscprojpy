# TODO: Version Support and Time Scaling

## Phase 1: Version Support
- [ ] Add version detection function to scaler.py
- [ ] Create VersionHandler class for compatibility
- [ ] Add version validation with appropriate error messages
- [ ] Implement version-specific property handling
- [ ] Add loguru errors for unsupported old versions
- [ ] Test with Camtasia 2020 (v4.0) files
- [ ] Test with Camtasia 2021+ (v9.0) files
- [ ] Update documentation with version support info

## Phase 2: Time Scaling Core Implementation
- [ ] Create TimeScaler class inheriting from TscprojScaler
- [ ] Define TIME_PROPERTIES set for time-related properties
- [ ] Implement _is_audio_media() detection method
- [ ] Create scale_time_value() method with media type awareness
- [ ] Implement special handling for audio clips
- [ ] Add keyframe time scaling
- [ ] Handle transition duration scaling
- [ ] Implement source range scaling

## Phase 3: CLI Integration
- [ ] Add timescale command to cli.py
- [ ] Make xyscale and timescale mutually exclusive
- [ ] Add scale parameter validation (positive, non-zero)
- [ ] Implement auto-generated output filenames for timescale
- [ ] Add progress indicators for time scaling
- [ ] Add verbose logging for time operations
- [ ] Test CLI interface

## Phase 4: Audio Handling
- [ ] Implement audio duration preservation logic
- [ ] Create audio repositioning algorithm
- [ ] Handle UnifiedMedia with audio tracks
- [ ] Test audio-only projects
- [ ] Test mixed media projects
- [ ] Validate audio sync after scaling

## Phase 5: Edge Cases and Validation
- [ ] Add overlap detection after time scaling
- [ ] Implement time value rounding for edit rate
- [ ] Handle negative time prevention
- [ ] Add validation for timeline integrity
- [ ] Test with complex multi-track projects
- [ ] Test with projects containing effects
- [ ] Handle fractional frame times

## Phase 6: Testing
- [ ] Create test_timescaler.py
- [ ] Write unit tests for time property detection
- [ ] Write tests for audio handling
- [ ] Test version detection and handling
- [ ] Create integration tests for timescale command
- [ ] Test with real-world project files
- [ ] Performance testing with large projects

## Phase 7: Documentation
- [ ] Update README.md with timescale examples
- [ ] Add version compatibility matrix
- [ ] Document audio handling behavior
- [ ] Create troubleshooting guide
- [ ] Update CHANGELOG.md
- [ ] Add examples to docs folder