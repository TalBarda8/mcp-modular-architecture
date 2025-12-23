"""
Unit tests for ResourceRegistry.
"""

import pytest
from src.mcp.resource_registry import ResourceRegistry
from src.mcp.resources.config_resource import ConfigResource
from src.mcp.resources.status_resource import StatusResource
from src.core.errors.exceptions import (
    ResourceAlreadyExistsError,
    ResourceNotFoundError
)


@pytest.mark.unit
class TestResourceRegistry:
    """Test suite for ResourceRegistry class."""

    @pytest.fixture
    def registry(self):
        """Create a fresh registry for each test."""
        reg = ResourceRegistry()
        reg.clear()
        return reg

    @pytest.fixture
    def config_resource(self):
        """Create a config resource instance."""
        return ConfigResource()

    @pytest.fixture
    def status_resource(self):
        """Create a status resource instance."""
        return StatusResource()

    def test_singleton_pattern(self):
        """Test that ResourceRegistry implements singleton pattern."""
        registry1 = ResourceRegistry()
        registry2 = ResourceRegistry()
        assert registry1 is registry2

    def test_register_resource(self, registry, config_resource):
        """Test registering a resource."""
        registry.register(config_resource)
        assert 'config://app' in registry
        assert len(registry) == 1

    def test_register_duplicate_resource_raises_error(
        self,
        registry,
        config_resource
    ):
        """Test that registering duplicate resource raises error."""
        registry.register(config_resource)

        with pytest.raises(ResourceAlreadyExistsError) as exc_info:
            registry.register(ConfigResource())
        assert 'config://app' in str(exc_info.value)

    def test_get_resource(self, registry, config_resource):
        """Test getting a registered resource."""
        registry.register(config_resource)
        resource = registry.get_resource('config://app')
        assert resource is config_resource

    def test_get_nonexistent_resource_raises_error(self, registry):
        """Test that getting non-existent resource raises error."""
        with pytest.raises(ResourceNotFoundError) as exc_info:
            registry.get_resource('nonexistent://resource')
        assert 'nonexistent://resource' in str(exc_info.value)

    def test_list_resources(self, registry, config_resource, status_resource):
        """Test listing all registered resources."""
        registry.register(config_resource)
        registry.register(status_resource)

        resources = registry.list_resources()
        assert len(resources) == 2
        assert 'config://app' in resources
        assert 'status://system' in resources

    def test_get_resources_metadata(self, registry, config_resource):
        """Test getting resources metadata."""
        registry.register(config_resource)

        metadata = registry.get_resources_metadata()
        assert len(metadata) == 1
        assert metadata[0]['uri'] == 'config://app'
        assert 'name' in metadata[0]

    def test_unregister_resource(self, registry, config_resource):
        """Test unregistering a resource."""
        registry.register(config_resource)
        assert 'config://app' in registry

        registry.unregister('config://app')
        assert 'config://app' not in registry
        assert len(registry) == 0

    def test_unregister_nonexistent_resource_raises_error(self, registry):
        """Test that unregistering non-existent resource raises error."""
        with pytest.raises(ResourceNotFoundError):
            registry.unregister('nonexistent://resource')

    def test_clear_registry(self, registry, config_resource, status_resource):
        """Test clearing all resources from registry."""
        registry.register(config_resource)
        registry.register(status_resource)
        assert len(registry) == 2

        registry.clear()
        assert len(registry) == 0

    def test_contains_operator(self, registry, config_resource):
        """Test the 'in' operator."""
        assert 'config://app' not in registry

        registry.register(config_resource)
        assert 'config://app' in registry
