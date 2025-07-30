# this_file: tests/test_serialization.py
"""Unit tests for serialization layer."""

import json
import tempfile
from pathlib import Path

import pytest

from tscprojpy.models import Project
from tscprojpy.serialization import (
    ProjectLoader,
    ProjectSaver,
    ProjectVersion,
    detect_version,
    is_supported_version,
    get_version_features,
)


class TestProjectVersion:
    """Test version detection and features."""
    
    def test_version_enum(self):
        """Test version enum values."""
        assert ProjectVersion.V4_0.value == "4.0"
        assert ProjectVersion.V9_0.value == "9.0"
        assert ProjectVersion.UNKNOWN.value == "unknown"
    
    def test_version_edit_rates(self):
        """Test version edit rates."""
        assert ProjectVersion.V4_0.edit_rate == 60
        assert ProjectVersion.V9_0.edit_rate == 705600000
        assert ProjectVersion.UNKNOWN.edit_rate == 60
    
    def test_version_support(self):
        """Test version support flags."""
        assert ProjectVersion.V4_0.is_supported
        assert ProjectVersion.V9_0.is_supported
        assert not ProjectVersion.UNKNOWN.is_supported
    
    def test_detect_version(self):
        """Test version detection from data."""
        assert detect_version({"version": "4.0"}) == ProjectVersion.V4_0
        assert detect_version({"version": "9.0"}) == ProjectVersion.V9_0
        assert detect_version({"version": "99.0"}) == ProjectVersion.UNKNOWN
        assert detect_version({}) == ProjectVersion.UNKNOWN
    
    def test_is_supported_version(self):
        """Test supported version check."""
        assert is_supported_version({"version": "4.0"})
        assert is_supported_version({"version": "9.0"})
        assert not is_supported_version({"version": "99.0"})
    
    def test_version_features(self):
        """Test version feature detection."""
        v4_features = get_version_features(ProjectVersion.V4_0)
        assert not v4_features["has_high_precision_timing"]
        assert not v4_features["has_loudness_normalization"]
        
        v9_features = get_version_features(ProjectVersion.V9_0)
        assert v9_features["has_high_precision_timing"]
        assert v9_features["has_loudness_normalization"]
        assert v9_features["has_authoring_client"]


class TestProjectLoader:
    """Test ProjectLoader."""
    
    def test_load_dict_basic(self):
        """Test loading project from dictionary."""
        data = {
            "version": "9.0",
            "editRate": 705600000,
            "width": 1920,
            "height": 1080,
            "videoFormatFrameRate": 30,
            "sourceBin": [],
            "timeline": {
                "id": 1,
                "sceneTrack": {
                    "scenes": [{
                        "csml": {
                            "tracks": []
                        }
                    }]
                }
            }
        }
        
        loader = ProjectLoader()
        project = loader.load_dict(data)
        
        assert project.version == "9.0"
        assert project.edit_rate == 705600000
        assert project.canvas.width == 1920
        assert project.canvas.height == 1080
    
    def test_load_dict_unsupported_version_strict(self):
        """Test loading unsupported version with strict checking."""
        data = {
            "version": "99.0",
            "width": 1920,
            "height": 1080,
            "sourceBin": [],
            "timeline": {"id": 1}
        }
        
        loader = ProjectLoader(strict_version_check=True)
        
        with pytest.raises(ValueError, match="Unsupported project version"):
            loader.load_dict(data)
    
    def test_load_dict_unsupported_version_lenient(self):
        """Test loading unsupported version with lenient checking."""
        data = {
            "version": "99.0",
            "editRate": 60,
            "width": 1920,
            "height": 1080,
            "videoFormatFrameRate": 30,
            "sourceBin": [],
            "timeline": {
                "id": 1,
                "sceneTrack": {"scenes": [{"csml": {"tracks": []}}]}
            }
        }
        
        loader = ProjectLoader(strict_version_check=False)
        project = loader.load_dict(data)  # Should not raise
        
        assert project.version == "99.0"
    
    def test_load_file(self):
        """Test loading project from file."""
        data = {
            "version": "9.0",
            "editRate": 705600000,
            "width": 1920,
            "height": 1080,
            "videoFormatFrameRate": 30,
            "sourceBin": [],
            "timeline": {
                "id": 1,
                "sceneTrack": {"scenes": [{"csml": {"tracks": []}}]}
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tscproj', delete=False) as f:
            json.dump(data, f)
            temp_path = Path(f.name)
        
        try:
            loader = ProjectLoader()
            project = loader.load_file(temp_path)
            
            assert project.version == "9.0"
            assert project.canvas.width == 1920
        finally:
            temp_path.unlink()
    
    def test_load_file_not_found(self):
        """Test loading non-existent file."""
        loader = ProjectLoader()
        
        with pytest.raises(FileNotFoundError):
            loader.load_file("/nonexistent/file.tscproj")
    
    def test_validate_structure(self):
        """Test structure validation."""
        loader = ProjectLoader()
        
        # Valid structure
        valid_data = {
            "version": "9.0",
            "editRate": 60,
            "width": 1920,
            "height": 1080,
            "sourceBin": [],
            "timeline": {"sceneTrack": {}}
        }
        errors = loader.validate_structure(valid_data)
        assert len(errors) == 0
        
        # Missing required fields for version 9.0
        invalid_data = {
            "version": "9.0",
            "width": 1920
        }
        errors = loader.validate_structure(invalid_data)
        assert "editRate" in str(errors)
        assert "height" in str(errors)
        
        # Wrong types
        wrong_type_data = {
            "version": "9.0",
            "editRate": 60,
            "width": 1920,
            "height": 1080,
            "sourceBin": "not a list",  # Should be list
            "timeline": []  # Should be dict
        }
        errors = loader.validate_structure(wrong_type_data)
        assert "sourceBin must be a list" in errors
        assert "timeline must be a dictionary" in errors


class TestProjectSaver:
    """Test ProjectSaver."""
    
    def test_save_project(self):
        """Test saving project."""
        project = Project.empty()
        saver = ProjectSaver()
        
        # Convert to dict
        data = saver.project_to_dict(project)
        
        assert "version" in data
        assert "width" in data
        assert "height" in data
        assert data["version"] == "9.0"
        assert data["width"] == 1920
    
    def test_save_file(self):
        """Test saving project to file."""
        project = Project.empty(width=3840, height=2160)
        saver = ProjectSaver()
        
        with tempfile.NamedTemporaryFile(suffix='.tscproj', delete=False) as f:
            temp_path = Path(f.name)
        
        try:
            saver.save_file(project, temp_path)
            
            # Verify file was created and can be loaded
            assert temp_path.exists()
            
            with open(temp_path) as f:
                data = json.load(f)
            
            assert data["width"] == 3840
            assert data["height"] == 2160
        finally:
            temp_path.unlink()
    
    def test_save_dict(self):
        """Test saving dictionary to file."""
        data = {"test": "data", "nested": {"value": 123}}
        saver = ProjectSaver()
        
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_path = Path(f.name)
        
        try:
            saver.save_dict(data, temp_path)
            
            with open(temp_path) as f:
                loaded = json.load(f)
            
            assert loaded == data
        finally:
            temp_path.unlink()
    
    def test_to_json_string(self):
        """Test converting project to JSON string."""
        project = Project.empty()
        saver = ProjectSaver(indent=4)
        
        json_str = saver.to_json_string(project)
        
        # Verify it's valid JSON
        data = json.loads(json_str)
        assert data["version"] == "9.0"
        
        # Check indentation
        assert "\n    " in json_str  # 4-space indent
    
    def test_save_options(self):
        """Test save options."""
        project = Project.empty()
        project.metadata.title = "Test — Unicode"
        
        # Test with ensure_ascii=True
        saver_ascii = ProjectSaver(ensure_ascii=True)
        json_ascii = saver_ascii.to_json_string(project)
        assert "\\u2014" in json_ascii  # Em dash escaped
        
        # Test with ensure_ascii=False
        saver_unicode = ProjectSaver(ensure_ascii=False)
        json_unicode = saver_unicode.to_json_string(project)
        assert "—" in json_unicode  # Em dash not escaped
    
    def test_round_trip(self):
        """Test save and load round trip."""
        # Create project with some data
        original = Project.empty(width=2560, height=1440, fps=60)
        original.metadata.title = "Test Project"
        original.metadata.author = "Test Author"
        
        with tempfile.NamedTemporaryFile(suffix='.tscproj', delete=False) as f:
            temp_path = Path(f.name)
        
        try:
            # Save
            saver = ProjectSaver()
            saver.save_file(original, temp_path)
            
            # Load
            loader = ProjectLoader()
            loaded = loader.load_file(temp_path)
            
            # Verify
            assert loaded.canvas.width == original.canvas.width
            assert loaded.canvas.height == original.canvas.height
            assert loaded.canvas.frame_rate == original.canvas.frame_rate
            assert loaded.metadata.title == original.metadata.title
            assert loaded.metadata.author == original.metadata.author
        finally:
            temp_path.unlink()