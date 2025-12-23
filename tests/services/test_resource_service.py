"""
Unit tests for ResourceService.
"""

import pytest
from src.services.resource_service import ResourceService
from src.core.errors.exceptions import (
    ResourceNotFoundError,
    ResourceAlreadyExistsError,
    ValidationError
)


@pytest.mark.unit
class TestResourceService:
    """Test suite for ResourceService class."""

    @pytest.fixture
    def service(self):
        """Create a fresh ResourceService instance for each test."""
        return ResourceService()

    def test_create_resource(self, service):
        """Test creating a new resource."""
        resource = service.create_resource(
            resource_id='test-1',
            name='Test Resource'
        )
        assert resource.resource_id == 'test-1'
        assert resource.name == 'Test Resource'

    def test_create_duplicate_resource_raises_error(self, service):
        """Test that creating duplicate resource raises error."""
        service.create_resource(resource_id='test-1', name='Test 1')

        with pytest.raises(ResourceAlreadyExistsError) as exc_info:
            service.create_resource(resource_id='test-1', name='Test 2')
        assert 'test-1' in str(exc_info.value)

    def test_create_invalid_resource_raises_error(self, service):
        """Test that invalid resource data raises ValidationError."""
        with pytest.raises(ValidationError):
            service.create_resource(resource_id='', name='Test')

    def test_get_existing_resource(self, service):
        """Test getting an existing resource."""
        service.create_resource(resource_id='test-1', name='Test')
        resource = service.get_resource('test-1')
        assert resource.resource_id == 'test-1'

    def test_get_nonexistent_resource_raises_error(self, service):
        """Test that getting non-existent resource raises error."""
        with pytest.raises(ResourceNotFoundError) as exc_info:
            service.get_resource('nonexistent')
        assert 'nonexistent' in str(exc_info.value)

    def test_list_resources(self, service):
        """Test listing all resources."""
        service.create_resource(resource_id='test-1', name='Test 1')
        service.create_resource(resource_id='test-2', name='Test 2')

        resources = service.list_resources()
        assert len(resources) == 2

    def test_list_resources_with_filter(self, service):
        """Test listing resources with status filter."""
        service.create_resource(
            resource_id='test-1',
            name='Test 1',
            status='active'
        )
        service.create_resource(
            resource_id='test-2',
            name='Test 2',
            status='inactive'
        )

        active_resources = service.list_resources(status_filter='active')
        assert len(active_resources) == 1
        assert active_resources[0].status == 'active'

    def test_delete_resource(self, service):
        """Test deleting a resource."""
        service.create_resource(resource_id='test-1', name='Test')
        service.delete_resource('test-1')

        with pytest.raises(ResourceNotFoundError):
            service.get_resource('test-1')

    def test_delete_nonexistent_resource_raises_error(self, service):
        """Test that deleting non-existent resource raises error."""
        with pytest.raises(ResourceNotFoundError):
            service.delete_resource('nonexistent')
