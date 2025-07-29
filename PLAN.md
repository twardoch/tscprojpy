# tscprojpy Implementation Plan

## Project Overview

`tscprojpy` is a Python package for manipulating Camtasia `.tscproj` project files. It provides programmatic access to video project data, enabling automated workflows for scaling, time manipulation, and project generation.

## Current State

### Implemented
- Basic `xyscale` command for spatial scaling
- Recursive JSON traversal and property detection
- CLI with Rich UI and progress indicators
- Comprehensive file format documentation

### Architecture Analysis
- **Strengths**: Clear separation, efficient property detection, good UX
- **Weaknesses**: No domain model, limited extensibility, tight coupling, no tests

## Target Architecture

### Layered Design

```
┌─────────────────────────────────────────────────────┐
│                   CLI Layer                         │
│        (Fire commands, Rich UI, arg parsing)        │
├─────────────────────────────────────────────────────┤
│                 Operations Layer                    │
│     (XYScaler, TimeScaler, ProjectAssembler)       │
├─────────────────────────────────────────────────────┤
│                  Model Layer                        │
│  (Project, Timeline, Track, Media, SourceItem)     │
├─────────────────────────────────────────────────────┤
│                Traversal Engine                     │
│      (Property visitor, transformation core)        │
├─────────────────────────────────────────────────────┤
│              Serialization Layer                    │
│         (JSON ↔ Model, validation, versions)       │
└─────────────────────────────────────────────────────┘
```

### Design Patterns
- **Domain-Driven Design**: Explicit Camtasia concepts
- **Visitor Pattern**: Separate traversal from transformation
- **Strategy Pattern**: Pluggable operations
- **Builder Pattern**: Project construction
- **Immutability**: Operations return new objects

## Implementation Roadmap

### Phase 1: Foundation Refactoring (Week 1-2)

#### 1.1 Domain Model
- Create model classes for Project, Canvas, Timeline, Media types
- Implement immutable transformations
- Add factory methods for common patterns

#### 1.2 Traversal Engine
- Build PropertyTransformer base class
- Implement SpatialTransformer for XY scaling
- Create TemporalTransformer for time scaling
- Add visitor pattern for extensibility

#### 1.3 Serialization Layer
- Version detection and normalization
- Model ↔ JSON conversion
- Validation framework

### Phase 2: Core Operations (Week 3)

#### 2.1 Refactor XYScale
- Use new domain model
- Leverage transformation engine
- Add validation

#### 2.2 Implement TimeScale
- Audio duration preservation
- Timeline repositioning
- Keyframe scaling

#### 2.3 Version Support
- Handle v4.0 (Camtasia 2020)
- Handle v9.0 (Camtasia 2021+)
- Graceful degradation for unknown versions

### Phase 3: Project Assembly (Week 4)

#### 3.1 Project Builder
- Fluent API for project creation
- Media management
- Timeline construction

#### 3.2 Templates
- Common project structures
- Reusable components
- Export/import templates

### Phase 4: Advanced Features (Week 5-6)

#### 4.1 Batch Processing
- Multiple file operations
- Pattern matching
- Progress tracking

#### 4.2 Analysis Tools
- Project statistics
- Complexity metrics
- Media inventory

#### 4.3 Effect Management
- Transition library
- Filter application
- Effect chaining

### Phase 5: Testing & Documentation (Week 7)

#### 5.1 Test Suite
- Unit tests for all components
- Integration tests for operations
- Property-based testing for transformations
- Regression tests with real files

#### 5.2 Documentation
- API reference
- Tutorial series
- Migration guide

## Technical Specifications

### Domain Model Structure

```python
Project
├── Canvas (width, height, fps)
├── SourceBin[]
│   └── SourceItem (id, path, type, metadata)
├── Timeline
│   ├── Tracks[]
│   │   └── Media[] (VideoMedia, AudioMedia, ImageMedia, Callout)
│   └── Transitions[]
└── Metadata (version, editRate, author)
```

### Operation Interface

```python
class Operation(ABC):
    @abstractmethod
    def execute(self, project: Project) -> Project:
        """Execute operation on project."""
    
    @abstractmethod
    def validate(self, project: Project) -> List[ValidationError]:
        """Pre-flight validation."""
```

### CLI Commands

Current:
- `xyscale` - Spatial scaling

Planned:
- `timescale` - Temporal scaling
- `create` - New project
- `info` - Project information
- `validate` - Integrity check
- `batch` - Multi-file processing
- `analyze` - Project statistics

## Quality Standards

### Code Quality
- Type hints on all public APIs
- Docstrings following Google style
- 90%+ test coverage
- Ruff linting compliance

### Performance Targets
- <2s for typical projects (10MB)
- <10s for large projects (100MB)
- Memory usage <3x file size

### Error Handling
- User-friendly error messages
- Detailed logging in verbose mode
- Graceful degradation
- No data loss

## Migration Strategy

1. **Parallel Development**: Build new architecture alongside current
2. **Feature Parity**: Match current functionality first
3. **Gradual Cutover**: Switch operations one at a time
4. **Compatibility Layer**: Support old CLI interface
5. **Deprecation Period**: 2 releases before removing old code

## Future Vision

### Near Term (3 months)
- Full domain model implementation
- Time scaling operation
- Basic project creation
- Comprehensive test suite

### Medium Term (6 months)
- Visual effect library
- Template marketplace
- Plugin system
- Performance optimizations

### Long Term (1 year)
- GUI application
- Cloud rendering integration
- AI-powered editing suggestions
- Real-time collaboration

## Success Metrics

- **Adoption**: 1000+ downloads/month
- **Reliability**: <1 bug report/month
- **Performance**: Meeting all targets
- **Extensibility**: <100 LOC for new operations
- **Community**: 10+ contributors