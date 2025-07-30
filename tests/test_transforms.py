# this_file: tests/test_transforms.py
"""Unit tests for transform engine."""

import pytest

from tscprojpy.models import Canvas, Project, ProjectMetadata, Timeline, Track, VideoMedia, AudioMedia
from tscprojpy.transforms import PropertyTransformer, TransformConfig, TransformType


class TestTransformConfig:
    """Test TransformConfig."""
    
    def test_spatial_config(self):
        """Test spatial transform config."""
        config = TransformConfig(
            transform_type=TransformType.SPATIAL,
            factor=2.0,
            verbose=True
        )
        assert config.transform_type == TransformType.SPATIAL
        assert config.factor == 2.0
        assert config.verbose
        assert config.preserve_audio_duration  # Default
    
    def test_temporal_config(self):
        """Test temporal transform config."""
        config = TransformConfig(
            transform_type=TransformType.TEMPORAL,
            factor=1.5,
            preserve_audio_duration=False
        )
        assert config.transform_type == TransformType.TEMPORAL
        assert config.factor == 1.5
        assert not config.preserve_audio_duration


class TestPropertyTransformer:
    """Test PropertyTransformer."""
    
    def test_spatial_transform_project(self):
        """Test spatial transformation of project."""
        project = Project.empty(width=1920, height=1080)
        
        config = TransformConfig(TransformType.SPATIAL, factor=2.0)
        transformer = PropertyTransformer(config)
        
        transformed = transformer.transform_project(project)
        
        assert transformed.canvas.width == 3840
        assert transformed.canvas.height == 2160
        assert project.canvas.width == 1920  # Original unchanged
    
    def test_temporal_transform_project(self):
        """Test temporal transformation of project."""
        # Create project with media
        project = Project.empty()
        track = Track(track_index=0)
        track.add_media(VideoMedia(id=1, src=1, start=100, duration=200))
        track.add_media(AudioMedia(id=2, src=2, start=300, duration=100))
        project.timeline.add_track(track)
        
        config = TransformConfig(TransformType.TEMPORAL, factor=2.0)
        transformer = PropertyTransformer(config)
        
        transformed = transformer.transform_project(project)
        
        # Check video scaled
        video = transformed.timeline.tracks[0].medias[0]
        assert video.start == 200
        assert video.duration == 400
        
        # Check audio duration preserved
        audio = transformed.timeline.tracks[0].medias[1]
        assert audio.start == 600  # Position scaled
        assert audio.duration == 100  # Duration preserved!
    
    def test_transform_dict_spatial(self):
        """Test spatial transformation of raw dictionary."""
        data = {
            "width": 1920,
            "height": 1080,
            "sourceBin": [{
                "rect": [0, 0, 1920, 1080],
                "sourceTracks": [{
                    "trackRect": [0, 0, 1920, 1080]
                }]
            }],
            "timeline": {
                "sceneTrack": {
                    "scenes": [{
                        "csml": {
                            "tracks": [{
                                "medias": [{
                                    "parameters": {
                                        "translation0": 100,
                                        "scale0": 1.0
                                    }
                                }]
                            }]
                        }
                    }]
                }
            }
        }
        
        config = TransformConfig(TransformType.SPATIAL, factor=2.0)
        transformer = PropertyTransformer(config)
        
        transformed = transformer.transform_dict(data)
        
        assert transformed["width"] == 3840
        assert transformed["height"] == 2160
        assert transformed["sourceBin"][0]["rect"] == [0, 0, 3840, 2160]
        assert transformed["timeline"]["sceneTrack"]["scenes"][0]["csml"]["tracks"][0]["medias"][0]["parameters"]["translation0"] == 200
    
    def test_transform_dict_temporal(self):
        """Test temporal transformation of raw dictionary."""
        data = {
            "timeline": {
                "sceneTrack": {
                    "scenes": [{
                        "csml": {
                            "tracks": [{
                                "medias": [
                                    {
                                        "_type": "VMFile",
                                        "start": 100,
                                        "duration": 200
                                    },
                                    {
                                        "_type": "AMFile",
                                        "start": 300,
                                        "duration": 100
                                    }
                                ]
                            }]
                        }
                    }]
                }
            }
        }
        
        config = TransformConfig(
            TransformType.TEMPORAL, 
            factor=2.0,
            preserve_audio_duration=True
        )
        transformer = PropertyTransformer(config)
        
        transformed = transformer.transform_dict(data)
        
        medias = transformed["timeline"]["sceneTrack"]["scenes"][0]["csml"]["tracks"][0]["medias"]
        
        # Video scaled
        assert medias[0]["start"] == 200
        assert medias[0]["duration"] == 400
        
        # Audio duration preserved
        assert medias[1]["start"] == 600
        assert medias[1]["duration"] == 100  # Preserved!
    
    def test_keyframe_scaling_spatial(self):
        """Test spatial scaling of keyframes."""
        # Need full structure for transform_dict
        data = {
            "timeline": {
                "sceneTrack": {
                    "scenes": [{
                        "csml": {
                            "tracks": [{
                                "medias": [{
                                    "parameters": {
                                        "translation0": {
                                            "keyframes": [
                                                {"time": 0, "value": 100},
                                                {"time": 100, "value": 200}
                                            ]
                                        }
                                    }
                                }]
                            }]
                        }
                    }]
                }
            }
        }
        
        config = TransformConfig(TransformType.SPATIAL, factor=2.0)
        transformer = PropertyTransformer(config)
        
        result = transformer.transform_dict(data)
        
        params = result["timeline"]["sceneTrack"]["scenes"][0]["csml"]["tracks"][0]["medias"][0]["parameters"]
        keyframes = params["translation0"]["keyframes"]
        assert keyframes[0]["value"] == 200
        assert keyframes[1]["value"] == 400
        # Times not changed in spatial transform
        assert keyframes[0]["time"] == 0
        assert keyframes[1]["time"] == 100
    
    def test_keyframe_scaling_temporal(self):
        """Test temporal scaling of keyframes."""
        data = {
            "parameters": {
                "translation0": {
                    "keyframes": [
                        {"time": 0, "value": 100},
                        {"time": 100, "value": 200}
                    ]
                }
            }
        }
        
        config = TransformConfig(TransformType.TEMPORAL, factor=2.0)
        transformer = PropertyTransformer(config)
        
        result = transformer._transform_dict_temporal(data)
        
        keyframes = result["parameters"]["translation0"]["keyframes"]
        # Values not changed in temporal transform
        assert keyframes[0]["value"] == 100
        assert keyframes[1]["value"] == 200
        # Times are scaled
        assert keyframes[0]["time"] == 0
        assert keyframes[1]["time"] == 200
    
    def test_invalid_transform_type(self):
        """Test invalid transform type raises error."""
        project = Project.empty()
        
        # Create config with invalid type by setting it after creation
        config = TransformConfig(TransformType.SPATIAL, factor=2.0)
        config.transform_type = "INVALID"  # type: ignore
        
        transformer = PropertyTransformer(config)
        
        with pytest.raises(ValueError, match="Unknown transform type"):
            transformer.transform_project(project)