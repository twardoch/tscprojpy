# tscprojpy Revised Implementation Plan

## Project Analysis

After implementing the initial xyscale functionality and analyzing the codebase, several architectural improvements are needed:

### Current Strengths
1. **Clear separation of concerns**: CLI and scaling logic are separate
2. **Recursive traversal works**: Handles nested structures effectively
3. **Property detection is efficient**: Set-based lookups are O(1)
4. **Good error handling**: User-friendly messages with Rich UI

### Current Weaknesses
1. **No domain model**: Direct JSON manipulation is fragile
2. **Limited extensibility**: Hard to add new operations
3. **No validation layer**: Could produce invalid output
4. **Tight coupling**: Scaling logic mixed with traversal
5. **No tests**: Critical for a data transformation tool

## Revised Architecture

### Layer Architecture

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

### Core Design Principles

1. **Domain-Driven Design**: Model Camtasia concepts explicitly
2. **Visitor Pattern**: Separate traversal from transformation logic
3. **Strategy Pattern**: Pluggable operations
4. **Builder Pattern**: For creating projects from scratch
5. **Immutability**: Operations return new objects, don't mutate

## Implementation Phases

### Phase 1: Domain Model (Week 1)

Create a proper object model for Camtasia projects:

```python
# models/project.py
@dataclass
class Project:
    title: str
    description: str
    author: str
    canvas: Canvas
    source_bin: List[SourceItem]
    timeline: Timeline
    metadata: ProjectMetadata
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Project':
        """Create from parsed JSON."""
        
    def to_dict(self) -> dict:
        """Convert to JSON-serializable dict."""

# models/canvas.py
@dataclass
class Canvas:
    width: float
    height: float
    frame_rate: int
    
    def scale(self, factor: float) -> 'Canvas':
        """Return scaled canvas."""
        return Canvas(
            width=self.width * factor,
            height=self.height * factor,
            frame_rate=self.frame_rate
        )

# models/media.py
class Media(ABC):
    """Base class for all media types."""
    
    @abstractmethod
    def scale_spatial(self, factor: float) -> 'Media':
        """Scale spatial properties."""
    
    @abstractmethod
    def scale_temporal(self, factor: float) -> 'Media':
        """Scale temporal properties."""

class VideoMedia(Media):
    """VMFile, ScreenVMFile implementations."""

class AudioMedia(Media):
    """AMFile implementation."""
    
    def scale_temporal(self, factor: float) -> 'AudioMedia':
        # Special handling: scale position, not duration
        return AudioMedia(
            start=self.start * factor,
            duration=self.duration,  # Preserved!
            ...
        )
```

### Phase 2: Traversal Engine (Week 1)

Implement a flexible property transformation system:

```python
# transform/engine.py
class PropertyTransformer:
    """Base transformer for property visitors."""
    
    def transform_project(self, project: Project) -> Project:
        """Transform entire project."""
        
    def transform_media(self, media: Media) -> Media:
        """Transform media item."""
        
    def transform_keyframes(self, keyframes: List[Keyframe]) -> List[Keyframe]:
        """Transform animation keyframes."""

# transform/spatial.py
class SpatialTransformer(PropertyTransformer):
    """Handles XY scaling transformations."""
    
    def __init__(self, scale_factor: float):
        self.scale_factor = scale_factor
    
    def transform_project(self, project: Project) -> Project:
        return Project(
            canvas=project.canvas.scale(self.scale_factor),
            timeline=self.transform_timeline(project.timeline),
            source_bin=[self.transform_source(s) for s in project.source_bin],
            ...
        )

# transform/temporal.py  
class TemporalTransformer(PropertyTransformer):
    """Handles time scaling transformations."""
    
    def transform_media(self, media: Media) -> Media:
        if isinstance(media, AudioMedia):
            return media.reposition(self.scale_factor)
        else:
            return media.scale_temporal(self.scale_factor)
```

### Phase 3: Serialization Layer (Week 1)

Handle version differences and validation:

```python
# serialization/parser.py
class ProjectParser:
    """Parses .tscproj files into domain models."""
    
    def parse(self, file_path: Path) -> Project:
        data = self._load_json(file_path)
        version = self._detect_version(data)
        
        if version < Version("4.0"):
            raise UnsupportedVersionError(f"Version {version} too old")
            
        normalizer = self._get_normalizer(version)
        normalized = normalizer.normalize(data)
        
        return Project.from_dict(normalized)

# serialization/validator.py
class ProjectValidator:
    """Validates project integrity."""
    
    def validate(self, project: Project) -> List[ValidationError]:
        errors = []
        
        # Check timeline consistency
        if not self._validate_timeline(project.timeline):
            errors.append(ValidationError("Timeline has gaps"))
            
        # Check media references
        if not self._validate_references(project):
            errors.append(ValidationError("Missing media references"))
            
        return errors
```

### Phase 4: Refactor Operations (Week 2)

Reimplement operations using the new architecture:

```python
# operations/xyscale.py
class XYScaleOperation:
    """Scales spatial properties of a project."""
    
    def __init__(self, scale_factor: float):
        self.transformer = SpatialTransformer(scale_factor)
        
    def execute(self, project: Project) -> Project:
        logger.info(f"Scaling project by {self.scale_factor}x")
        
        scaled = self.transformer.transform_project(project)
        
        # Validate result
        validator = ProjectValidator()
        errors = validator.validate(scaled)
        if errors:
            logger.warning(f"Validation issues: {errors}")
            
        return scaled

# operations/timescale.py
class TimeScaleOperation:
    """Scales temporal properties of a project."""
    
    def __init__(self, scale_factor: float):
        self.transformer = TemporalTransformer(scale_factor)
        
    def execute(self, project: Project) -> Project:
        # Implementation
```

### Phase 5: Project Assembly (Week 2)

Enable creating projects from scratch:

```python
# builders/project_builder.py
class ProjectBuilder:
    """Fluent interface for building projects."""
    
    def __init__(self):
        self._reset()
        
    def _reset(self):
        self._project = Project()
        
    def set_canvas(self, width: int, height: int, fps: int = 30):
        self._project.canvas = Canvas(width, height, fps)
        return self
        
    def add_video(self, path: str, start: float = 0, track: int = 0):
        source = SourceItem.from_file(path)
        self._project.source_bin.append(source)
        
        media = VideoMedia(source_id=source.id, start=start)
        self._project.timeline.tracks[track].add_media(media)
        return self
        
    def add_text(self, text: str, duration: float, **style):
        callout = Callout.text(text, **style)
        self._project.timeline.add_annotation(callout, duration)
        return self
        
    def build(self) -> Project:
        project = self._project
        self._reset()
        return project

# Example usage:
project = (ProjectBuilder()
    .set_canvas(1920, 1080, 60)
    .add_video("intro.mp4")
    .add_text("Welcome!", duration=3.0, font_size=48)
    .add_video("main.mp4", start=3.0)
    .build())
```

### Phase 6: Enhanced CLI (Week 3)

Upgrade the CLI with new commands:

```python
# cli.py
def xyscale(input: str, scale: float, output: str = None, **kwargs):
    """Scale spatial dimensions."""
    project = ProjectParser().parse(input)
    operation = XYScaleOperation(scale / 100.0)
    result = operation.execute(project)
    ProjectSerializer().save(result, output or _auto_filename(input, scale))

def timescale(input: str, scale: float, output: str = None, **kwargs):
    """Scale playback speed."""
    # Implementation

def create(output: str, width: int = 1920, height: int = 1080):
    """Create a new empty project."""
    project = (ProjectBuilder()
        .set_canvas(width, height)
        .build())
    ProjectSerializer().save(project, output)

def info(input: str):
    """Display project information."""
    project = ProjectParser().parse(input)
    console.print(Panel(
        f"Canvas: {project.canvas.width}x{project.canvas.height}\n"
        f"Duration: {project.timeline.duration}s\n"
        f"Tracks: {len(project.timeline.tracks)}\n"
        f"Media items: {project.timeline.media_count}"
    ))

def validate(input: str):
    """Check project integrity."""
    project = ProjectParser().parse(input)
    errors = ProjectValidator().validate(project)
    if errors:
        console.print("[red]Validation errors found:[/red]")
        for error in errors:
            console.print(f"  • {error}")
    else:
        console.print("[green]✓ Project is valid[/green]")
```

### Phase 7: Testing Suite (Week 3)

Comprehensive test coverage:

```python
# tests/test_models.py
def test_canvas_scaling():
    canvas = Canvas(1920, 1080, 30)
    scaled = canvas.scale(1.5)
    assert scaled.width == 2880
    assert scaled.height == 1620
    assert scaled.frame_rate == 30  # Unchanged

# tests/test_operations.py
def test_xyscale_operation():
    project = load_test_project("sample.tscproj")
    operation = XYScaleOperation(2.0)
    result = operation.execute(project)
    
    assert result.canvas.width == project.canvas.width * 2
    # More assertions...

# tests/test_builders.py
def test_project_builder():
    project = (ProjectBuilder()
        .set_canvas(1920, 1080)
        .add_video("test.mp4")
        .build())
    
    assert project.canvas.width == 1920
    assert len(project.source_bin) == 1
    assert len(project.timeline.tracks[0].medias) == 1
```

## Advanced Features

### 1. Batch Processing

```python
def batch(pattern: str, operation: str, **kwargs):
    """Process multiple files."""
    files = Path.glob(pattern)
    for file in files:
        console.print(f"Processing {file}...")
        # Apply operation
```

### 2. Project Analysis

```python
class ProjectAnalyzer:
    """Extract statistics and insights."""
    
    def analyze(self, project: Project) -> Report:
        return Report(
            duration=project.timeline.duration,
            media_types=self._count_media_types(project),
            effects_used=self._list_effects(project),
            complexity_score=self._calculate_complexity(project)
        )
```

### 3. Effect Management

```python
class EffectLibrary:
    """Manage and apply effects."""
    
    def apply_transition(self, media1: Media, media2: Media, 
                        transition_type: str, duration: float):
        """Add transition between clips."""
        
    def apply_filter(self, media: Media, filter_type: str, **params):
        """Apply visual filter to media."""
```

### 4. Template System

```python
class ProjectTemplate:
    """Reusable project structures."""
    
    @classmethod
    def youtube_intro(cls, title: str, logo_path: str) -> Project:
        """Generate YouTube intro template."""
        return (ProjectBuilder()
            .set_canvas(1920, 1080, 30)
            .add_video(logo_path, duration=2.0)
            .add_text(title, start=0.5, duration=1.5)
            .add_transition("fade", duration=0.5)
            .build())
```

## Migration Path

1. **Keep current code working**: Don't break existing functionality
2. **Gradual refactoring**: Build new architecture alongside old
3. **Feature parity first**: Ensure new system matches current features
4. **Deprecation period**: Give users time to migrate
5. **Clear upgrade path**: Document changes and benefits

## Success Metrics

- **Code coverage**: >90% test coverage
- **Performance**: <2s for typical projects, <10s for large ones
- **Reliability**: Zero data loss, validated output
- **Extensibility**: New operations in <100 lines of code
- **Usability**: Clear errors, helpful documentation
- **Compatibility**: Support Camtasia 2020-2025+