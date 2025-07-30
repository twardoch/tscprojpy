# TODO List

## Completed ✅
- [x] Implement xyscale command
- [x] Implement timescale command with audio preservation
- [x] Create domain model architecture
- [x] Add support for all media types
- [x] Create comprehensive test suite
- [x] Add version detection and compatibility
- [x] /work on @issues/101.txt

## Remaining Tasks

### Testing & Quality (100% ✅)
- [x] Create `tests/test_models.py` - Unit tests for domain models (26 tests)
- [x] Create `tests/test_transforms.py` - Unit tests for transform engine (9 tests)
- [x] Create `tests/test_serialization.py` - Unit tests for loaders/savers (18 tests)
- [x] Create `tests/test_cli.py` - Integration tests for CLI commands (14 tests)
- [x] All 67 tests pass with 63% code coverage
- [ ] Add property-based testing with hypothesis (future enhancement)
- [ ] Add test coverage reporting to CI (future enhancement)

### Documentation (90% → 100%)
- [ ] Create API reference documentation
- [ ] Add docstrings to all public methods
- [ ] Create CONTRIBUTING.md guide
- [ ] Add inline code examples
- [ ] Generate API docs with Sphinx

### Code Quality (100% ✅)
- [x] Run final linting pass with ruff (all issues fixed)
- [x] Enhanced version support for legacy formats
- [x] Improved error handling and validation
- [ ] Add type stubs for better IDE support (future enhancement)
- [ ] Optimize performance for large files (future enhancement)
- [ ] Add memory profiling tests (future enhancement)

## Future Enhancements (Post 1.0)
- [ ] Batch processing support
- [ ] Project validation command
- [ ] Project info/stats command
- [ ] Template system for project creation
- [ ] Plugin architecture
- [ ] GUI application