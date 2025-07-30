# this_file: tests/test_models.py
"""Unit tests for domain models."""

import pytest

from tscprojpy.models import (
    Canvas,
    Project,
    ProjectMetadata,
    SourceBin,
    SourceItem,
    SourceTrack,
    Timeline,
    Track,
    VideoMedia,
    AudioMedia,
    ImageMedia,
    Callout,
)


class TestCanvas:
    """Test Canvas model."""
    
    def test_create_canvas(self):
        """Test canvas creation."""
        canvas = Canvas(width=1920, height=1080, frame_rate=30)
        assert canvas.width == 1920
        assert canvas.height == 1080
        assert canvas.frame_rate == 30
    
    def test_canvas_immutable(self):
        """Test canvas is immutable."""
        canvas = Canvas(1920, 1080)
        with pytest.raises(AttributeError):
            canvas.width = 3840
    
    def test_canvas_scale(self):
        """Test canvas scaling."""
        canvas = Canvas(1920, 1080, 30)
        scaled = canvas.scale(2.0)
        
        assert scaled.width == 3840
        assert scaled.height == 2160
        assert scaled.frame_rate == 30  # Frame rate doesn't scale
        assert canvas.width == 1920  # Original unchanged
    
    def test_canvas_resize(self):
        """Test canvas resizing."""
        canvas = Canvas(1920, 1080)
        resized = canvas.resize(width=3840)
        
        assert resized.width == 3840
        assert resized.height == 1080
    
    def test_canvas_properties(self):
        """Test canvas computed properties."""
        landscape = Canvas(1920, 1080)
        assert landscape.aspect_ratio == pytest.approx(16/9)
        assert landscape.is_landscape
        assert not landscape.is_portrait
        assert not landscape.is_square
        
        portrait = Canvas(1080, 1920)
        assert portrait.is_portrait
        
        square = Canvas(1080, 1080)
        assert square.is_square
    
    def test_canvas_serialization(self):
        """Test canvas to/from dict."""
        canvas = Canvas(1920, 1080, 60)
        data = canvas.to_dict()
        
        assert data == {
            "width": 1920,
            "height": 1080,
            "videoFormatFrameRate": 60
        }
        
        restored = Canvas.from_dict(data)
        assert restored.width == canvas.width
        assert restored.height == canvas.height
        assert restored.frame_rate == canvas.frame_rate
    
    def test_standard_sizes(self):
        """Test standard canvas sizes."""
        sizes = Canvas.standard_sizes()
        assert "1080p" in sizes
        assert sizes["1080p"].width == 1920
        assert sizes["1080p"].height == 1080
        assert sizes["4K"].width == 3840


class TestSourceTrack:
    """Test SourceTrack model."""
    
    def test_create_source_track(self):
        """Test source track creation."""
        track = SourceTrack(
            range=[0, 1000],
            type=0,  # video
            edit_rate=60,
            track_rect=[0, 0, 1920, 1080]
        )
        assert track.is_video
        assert not track.is_audio
        assert not track.is_image
    
    def test_source_track_types(self):
        """Test track type detection."""
        video = SourceTrack(range=[0, 100], type=0, edit_rate=60, track_rect=[0, 0, 100, 100])
        assert video.is_video
        
        image = SourceTrack(range=[0, 100], type=1, edit_rate=60, track_rect=[0, 0, 100, 100])
        assert image.is_image
        
        audio = SourceTrack(range=[0, 100], type=2, edit_rate=60, track_rect=[0, 0, 0, 0])
        assert audio.is_audio
    
    def test_source_track_serialization(self):
        """Test source track serialization."""
        track = SourceTrack(
            range=[0, 1000],
            type=0,
            edit_rate=60,
            track_rect=[0, 0, 1920, 1080],
            sample_rate=48000,
            bit_depth=16,
            num_channels=2
        )
        data = track.to_dict()
        restored = SourceTrack.from_dict(data)
        
        assert restored.range == track.range
        assert restored.type == track.type
        assert restored.edit_rate == track.edit_rate


class TestSourceItem:
    """Test SourceItem model."""
    
    def test_create_source_item(self):
        """Test source item creation."""
        item = SourceItem(
            id=1,
            src="/path/to/video.mp4",
            rect=[0, 0, 1920, 1080],
            last_mod="2025-01-29T12:00:00Z"
        )
        assert item.id == 1
        assert item.width == 1920
        assert item.height == 1080
    
    def test_source_item_scale(self):
        """Test source item spatial scaling."""
        track = SourceTrack([0, 100], 0, 60, [0, 0, 100, 100])
        item = SourceItem(
            id=1,
            src="test.mp4",
            rect=[0, 0, 1920, 1080],
            last_mod="2025-01-29",
            source_tracks=[track]
        )
        
        scaled = item.scale_spatial(2.0)
        assert scaled.rect == [0, 0, 3840, 2160]
        assert scaled.source_tracks[0].track_rect == [0, 0, 200, 200]
        assert item.rect == [0, 0, 1920, 1080]  # Original unchanged
    
    def test_source_item_media_detection(self):
        """Test media type detection."""
        video_track = SourceTrack([0, 100], 0, 60, [0, 0, 100, 100])
        audio_track = SourceTrack([0, 100], 2, 60, [0, 0, 0, 0])
        
        video_item = SourceItem(1, "test.mp4", [0, 0, 100, 100], "2025", [video_track])
        assert video_item.has_video
        assert not video_item.has_audio
        
        av_item = SourceItem(2, "test.mp4", [0, 0, 100, 100], "2025", [video_track, audio_track])
        assert av_item.has_video
        assert av_item.has_audio


class TestMedia:
    """Test Media hierarchy."""
    
    def test_video_media_scale_spatial(self):
        """Test video media spatial scaling."""
        media = VideoMedia(
            id=1,
            src=1,
            parameters={"translation0": 100, "scale0": 1.0}
        )
        
        scaled = media.scale_spatial(2.0)
        assert scaled.parameters["translation0"] == 200
        assert scaled.parameters["scale0"] == 2.0
    
    def test_video_media_scale_temporal(self):
        """Test video media temporal scaling."""
        media = VideoMedia(
            id=1,
            src=1,
            start=100,
            duration=200,
            media_start=0,
            media_duration=200
        )
        
        scaled = media.scale_temporal(2.0)
        assert scaled.start == 200
        assert scaled.duration == 400
        assert scaled.media_start == 0
        assert scaled.media_duration == 400
    
    def test_audio_media_preserves_duration(self):
        """Test audio media preserves duration on temporal scale."""
        media = AudioMedia(
            id=1,
            src=2,
            start=100,
            duration=200,
            media_start=0,
            media_duration=200
        )
        
        scaled = media.scale_temporal(2.0)
        assert scaled.start == 200  # Position scaled
        assert scaled.duration == 200  # Duration preserved!
        assert scaled.media_duration == 200  # Media duration preserved!
    
    def test_callout_creation(self):
        """Test callout creation."""
        callout = Callout.text("Hello World", font_size=36, color="#FF0000")
        assert callout.definition["text"] == "Hello World"
        assert callout.definition["font-size"] == 36
        assert callout.definition["color"] == "#FF0000"
    
    def test_callout_scale_spatial(self):
        """Test callout spatial scaling."""
        callout = Callout(
            id=1,
            src=0,
            definition={"width": 100, "height": 50, "corner-radius": 5}
        )
        
        scaled = callout.scale_spatial(2.0)
        assert scaled.definition["width"] == 200
        assert scaled.definition["height"] == 100
        assert scaled.definition["corner-radius"] == 10


class TestTimeline:
    """Test Timeline and Track models."""
    
    def test_create_timeline(self):
        """Test timeline creation."""
        timeline = Timeline(id=1)
        assert timeline.id == 1
        assert timeline.track_count == 0
        assert timeline.duration == 0
    
    def test_timeline_with_tracks(self):
        """Test timeline with tracks."""
        track1 = Track(track_index=0)
        track1.add_media(VideoMedia(id=1, src=1, start=0, duration=100))
        
        track2 = Track(track_index=1)
        track2.add_media(VideoMedia(id=2, src=2, start=50, duration=150))
        
        timeline = Timeline(id=1, tracks=[track1, track2])
        
        assert timeline.track_count == 2
        assert timeline.media_count == 2
        assert timeline.duration == 200  # Max end time
    
    def test_track_scale_temporal(self):
        """Test track temporal scaling."""
        media = VideoMedia(id=1, src=1, start=100, duration=200)
        track = Track(track_index=0, medias=[media])
        
        scaled = track.scale_temporal(2.0)
        assert scaled.medias[0].start == 200
        assert scaled.medias[0].duration == 400


class TestProject:
    """Test Project model."""
    
    def test_create_empty_project(self):
        """Test creating empty project."""
        project = Project.empty()
        assert project.canvas.width == 1920
        assert project.canvas.height == 1080
        assert project.version == "9.0"
    
    def test_project_metadata(self):
        """Test project metadata."""
        metadata = ProjectMetadata(
            title="Test Project",
            author="Test Author",
            version="9.0"
        )
        assert metadata.title == "Test Project"
        assert metadata.edit_rate == 705600000  # Default
    
    def test_project_scale_spatial(self):
        """Test project spatial scaling."""
        project = Project.empty(width=1920, height=1080)
        scaled = project.scale_spatial(2.0)
        
        assert scaled.canvas.width == 3840
        assert scaled.canvas.height == 2160
        assert project.canvas.width == 1920  # Original unchanged
    
    def test_project_serialization(self):
        """Test project serialization."""
        project = Project.empty()
        data = project.to_dict()
        
        assert "version" in data
        assert "width" in data
        assert "height" in data
        assert "sourceBin" in data
        assert "timeline" in data
        
        restored = Project.from_dict(data)
        assert restored.canvas.width == project.canvas.width
        assert restored.version == project.version
    
    def test_project_duration(self):
        """Test project duration calculation."""
        project = Project.empty()
        assert project.duration == 0.0
        
        # Add media to timeline
        track = Track(track_index=0)
        track.add_media(VideoMedia(
            id=1, src=1, start=0, 
            duration=project.edit_rate * 10  # 10 seconds
        ))
        project.timeline.add_track(track)
        
        assert project.duration == pytest.approx(10.0)