# TODO List

## Completed Tasks

### Phase 1: Core Scaling Functionality ✓
- [x] Create `src/tscprojpy/scaler.py` module
- [x] Implement JSON loading function
- [x] Implement recursive property traversal
- [x] Implement property identification logic
- [x] Implement scaling rules for different property types
- [x] Add proper error handling for JSON parsing

### Phase 2: CLI Implementation ✓
- [x] Update `cli.py` with `xyscale` command
- [x] Add input file parameter handling
- [x] Add output file parameter handling
- [x] Add scale factor parameter handling
- [x] Implement auto-generated output filename logic
- [x] Add Rich progress indicators
- [x] Add input validation

### Phase 4: Documentation ✓
- [x] Update README.md with usage examples
- [x] Add comprehensive docstrings
- [x] Add type hints throughout
- [x] Implement verbose logging mode
- [x] Run linting and formatting
- [x] Create CHANGELOG.md entry
- [x] Create comprehensive .tscproj format documentation
- [x] Analyze 200+ example files for format understanding

## Remaining Tasks

### Phase 3: Testing
- [ ] Create `tests/test_scaler.py`
- [ ] Write unit tests for scaling functions
- [ ] Write tests for property identification
- [ ] Create `tests/test_cli.py`
- [ ] Write integration tests for CLI
- [ ] Test edge cases and error conditions

## Future Enhancements
- [ ] Add version compatibility checks
- [ ] Implement timescale operation
- [ ] Add batch processing support
- [ ] Add preview mode