"""
Unit tests for Resource model.
"""

import pytest
from src.models.resource import Resource
from src.core.errors.exceptions import ValidationError


@pytest.mark.unit
class TestResource:
    """Test suite for Resource model class."""

    def test_create_valid_resource(self):
        """Test creating a valid resource."""
        resource = Resource(
            resource_id='test-1',
            name='Test Resource'
        )
        assert resource.resource_id == 'test-1'
        assert resource.name == 'Test Resource'
        assert resource.status == 'active'
        assert resource.created_at is not None

    def test_create_resource_with_metadata(self):
        """Test creating a resource with metadata."""
        metadata = {'key': 'value', 'count': 42}
        resource = Resource(
            resource_id='test-2',
            name='Test Resource',
            metadata=metadata
        )
        assert resource.metadata == metadata

    def test_invalid_resource_id_raises_error(self):
        """Test that empty resource_id raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Resource(resource_id='', name='Test')
        assert 'resource_id' in str(exc_info.value)

    def test_invalid_name_raises_error(self):
        """Test that empty name raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Resource(resource_id='test-1', name='')
        assert 'name' in str(exc_info.value)

    def test_invalid_status_raises_error(self):
        """Test that invalid status raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            Resource(
                resource_id='test-1',
                name='Test',
                status='invalid'
            )
        assert 'status' in str(exc_info.value)

    def test_activate_resource(self):
        """Test activating a resource."""
        resource = Resource(
            resource_id='test-1',
            name='Test',
            status='inactive'
        )
        resource.activate()
        assert resource.status == 'active'

    def test_deactivate_resource(self):
        """Test deactivating a resource."""
        resource = Resource(
            resource_id='test-1',
            name='Test',
            status='active'
        )
        resource.deactivate()
        assert resource.status == 'inactive'

    def test_to_dict(self):
        """Test converting resource to dictionary."""
        resource = Resource(
            resource_id='test-1',
            name='Test Resource'
        )
        data = resource.to_dict()
        assert isinstance(data, dict)
        assert data['resource_id'] == 'test-1'
        assert data['name'] == 'Test Resource'
        assert 'created_at' in data
        assert 'updated_at' in data
