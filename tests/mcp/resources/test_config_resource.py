"""
Unit tests for ConfigResource.
"""

import pytest
from src.mcp.resources.config_resource import ConfigResource


@pytest.mark.unit
class TestConfigResource:
    """Test suite for ConfigResource class."""

    @pytest.fixture
    def resource(self):
        """Create a config resource instance."""
        return ConfigResource()

    def test_resource_metadata(self, resource):
        """Test resource metadata."""
        assert resource.uri == "config://app"
        assert resource.name == "Application Configuration"
        assert "configuration" in resource.description.lower()
        assert resource.mime_type == "application/json"

    def test_is_static_resource(self, resource):
        """Test that config resource is static."""
        assert resource.is_dynamic() is False

    def test_read_resource(self, resource):
        """Test reading config resource."""
        content = resource.read()

        assert isinstance(content, dict)
        assert 'uri' in content
        assert 'mimeType' in content
        assert 'content' in content
        assert content['uri'] == "config://app"

    def test_read_returns_config_data(self, resource):
        """Test that read returns actual configuration data."""
        content = resource.read()

        config_data = content['content']
        assert isinstance(config_data, dict)
        # Should contain app configuration
        assert 'app' in config_data or 'logging' in config_data

    def test_get_metadata(self, resource):
        """Test getting resource metadata."""
        metadata = resource.get_metadata()

        assert metadata['uri'] == "config://app"
        assert metadata['name'] == "Application Configuration"
        assert metadata['isDynamic'] is False

    def test_to_dict(self, resource):
        """Test resource to_dict method."""
        resource_dict = resource.to_dict()

        assert isinstance(resource_dict, dict)
        assert resource_dict['uri'] == "config://app"
