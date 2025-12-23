"""
Resource Registry for managing MCP resources.
Provides centralized registration and discovery of available resources.
"""

from typing import Dict, List, Optional

from src.mcp.resources.base_resource import BaseResource
from src.core.logging.logger import Logger
from src.core.errors.exceptions import (
    ResourceAlreadyExistsError,
    ResourceNotFoundError
)


class ResourceRegistry:
    """
    Registry for managing available MCP resources.

    Provides:
    - Resource registration and unregistration
    - Resource discovery by URI
    - Listing all available resources
    - Resource metadata access

    Implements singleton pattern to ensure single source of truth.
    """

    _instance: Optional['ResourceRegistry'] = None
    _resources: Dict[str, BaseResource] = {}

    def __new__(cls) -> 'ResourceRegistry':
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the resource registry."""
        self.logger = Logger.get_logger(__name__)

    def register(self, resource: BaseResource) -> None:
        """
        Register a resource in the registry.

        Args:
            resource: Resource instance to register

        Raises:
            ResourceAlreadyExistsError: If resource with same URI exists
        """
        resource_uri = resource.uri

        if resource_uri in self._resources:
            raise ResourceAlreadyExistsError(
                f"Resource '{resource_uri}' is already registered",
                {'resource_uri': resource_uri}
            )

        self._resources[resource_uri] = resource
        resource_type = "dynamic" if resource.is_dynamic() else "static"
        self.logger.info(f"Registered {resource_type} resource: {resource_uri}")

    def unregister(self, resource_uri: str) -> None:
        """
        Unregister a resource from the registry.

        Args:
            resource_uri: URI of resource to unregister

        Raises:
            ResourceNotFoundError: If resource not found
        """
        if resource_uri not in self._resources:
            raise ResourceNotFoundError(
                f"Resource '{resource_uri}' not found in registry",
                {'resource_uri': resource_uri}
            )

        del self._resources[resource_uri]
        self.logger.info(f"Unregistered resource: {resource_uri}")

    def get_resource(self, resource_uri: str) -> BaseResource:
        """
        Get a resource by URI.

        Args:
            resource_uri: URI of the resource

        Returns:
            Resource instance

        Raises:
            ResourceNotFoundError: If resource not found
        """
        if resource_uri not in self._resources:
            raise ResourceNotFoundError(
                f"Resource '{resource_uri}' not found in registry",
                {'resource_uri': resource_uri}
            )

        return self._resources[resource_uri]

    def list_resources(self) -> List[str]:
        """
        List all registered resource URIs.

        Returns:
            List of resource URIs
        """
        return list(self._resources.keys())

    def get_resources_metadata(self) -> List[Dict]:
        """
        Get metadata for all registered resources.

        Returns:
            List of resource metadata dictionaries
        """
        return [resource.to_dict() for resource in self._resources.values()]

    def clear(self) -> None:
        """
        Clear all registered resources.

        Useful for testing and cleanup.
        """
        self._resources.clear()
        self.logger.info("Cleared all resources from registry")

    def __len__(self) -> int:
        """Return the number of registered resources."""
        return len(self._resources)

    def __contains__(self, resource_uri: str) -> bool:
        """Check if a resource is registered."""
        return resource_uri in self._resources
