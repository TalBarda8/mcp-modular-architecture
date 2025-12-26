"""
Unit tests for StatusResource.
"""

import pytest
from src.mcp.resources.status_resource import StatusResource


@pytest.mark.unit
class TestStatusResource:
    """Test suite for StatusResource class."""

    @pytest.fixture
    def resource(self):
        """Create a status resource instance."""
        return StatusResource()

    def test_resource_metadata(self, resource):
        """Test resource metadata."""
        assert resource.uri == "status://system"
        assert resource.name == "System Status"
        assert "status" in resource.description.lower()
        assert resource.mime_type == "application/json"

    def test_is_dynamic_resource(self, resource):
        """Test that status resource is dynamic."""
        assert resource.is_dynamic() is True

    def test_read_resource(self, resource):
        """Test reading status resource."""
        content = resource.read()

        assert isinstance(content, dict)
        assert 'uri' in content
        assert 'mimeType' in content
        assert 'content' in content
        assert content['uri'] == "status://system"

    def test_read_returns_status_data(self, resource):
        """Test that read returns status data with timestamp."""
        content = resource.read()

        status_data = content['content']
        assert isinstance(status_data, dict)
        assert 'timestamp' in status_data
        assert 'status' in status_data
        assert 'read_count' in status_data

    def test_dynamic_behavior(self, resource):
        """Test that resource content changes with each read."""
        # Read multiple times
        content1 = resource.read()
        content2 = resource.read()
        content3 = resource.read()

        # Read counts should be different
        count1 = content1['content']['read_count']
        count2 = content2['content']['read_count']
        count3 = content3['content']['read_count']

        assert count1 < count2 < count3

    def test_get_metadata(self, resource):
        """Test getting resource metadata."""
        metadata = resource.get_metadata()

        assert metadata['uri'] == "status://system"
        assert metadata['name'] == "System Status"
        assert metadata['isDynamic'] is True

    def test_to_dict_includes_metadata(self):
        """Test to_dict includes all metadata."""
        resource = StatusResource()
        dict_repr = resource.to_dict()

        assert 'uri' in dict_repr
        assert 'name' in dict_repr
        assert 'description' in dict_repr
        assert 'mimeType' in dict_repr
        assert 'isDynamic' in dict_repr
        assert dict_repr['isDynamic'] is True
