"""
Resource service for managing Resource entities.
Demonstrates service layer and separation of concerns.
"""

from typing import Any, Dict, List, Optional
from src.models.resource import Resource
from src.core.logging.logger import Logger
from src.core.errors.exceptions import (
    ResourceNotFoundError,
    ResourceAlreadyExistsError,
    ValidationError
)
from src.core.errors.error_handler import ErrorHandler


class ResourceService:
    """
    Service for managing Resource entities.

    Provides CRUD operations and business logic for resources.
    Demonstrates separation between domain models and business logic.
    """

    def __init__(self):
        """Initialize the resource service."""
        self.logger = Logger.get_logger(__name__)
        self.error_handler = ErrorHandler(__name__)
        self._resources: Dict[str, Resource] = {}

    def create_resource(
        self,
        resource_id: str,
        name: str,
        status: str = 'active',
        metadata: Optional[Dict[str, Any]] = None
    ) -> Resource:
        """
        Create a new resource.

        Args:
            resource_id: Unique identifier for the resource
            name: Resource name
            status: Resource status
            metadata: Additional metadata

        Returns:
            Created resource instance

        Raises:
            ResourceAlreadyExistsError: If resource with ID already exists
            ValidationError: If resource data is invalid
        """
        self.logger.info(f"Creating resource: {resource_id}")

        if resource_id in self._resources:
            error = ResourceAlreadyExistsError(
                f"Resource with ID '{resource_id}' already exists",
                {'resource_id': resource_id}
            )
            self.error_handler.handle_error(error, reraise=True)

        try:
            resource = Resource(resource_id, name, status, metadata)
            self._resources[resource_id] = resource
            self.logger.info(f"Successfully created resource: {resource_id}")
            return resource
        except ValidationError as e:
            self.error_handler.handle_error(
                e,
                context={'resource_id': resource_id},
                reraise=True
            )
            raise  # For type checker

    def get_resource(self, resource_id: str) -> Resource:
        """
        Get a resource by ID.

        Args:
            resource_id: Resource identifier

        Returns:
            Resource instance

        Raises:
            ResourceNotFoundError: If resource not found
        """
        self.logger.debug(f"Fetching resource: {resource_id}")

        if resource_id not in self._resources:
            error = ResourceNotFoundError(
                f"Resource with ID '{resource_id}' not found",
                {'resource_id': resource_id}
            )
            self.error_handler.handle_error(error, reraise=True)

        return self._resources[resource_id]

    def list_resources(self, status_filter: Optional[str] = None) -> List[Resource]:
        """
        List all resources, optionally filtered by status.

        Args:
            status_filter: Optional status to filter by

        Returns:
            List of resources
        """
        self.logger.debug(f"Listing resources (filter: {status_filter})")

        resources = list(self._resources.values())

        if status_filter:
            resources = [r for r in resources if r.status == status_filter]

        return resources

    def delete_resource(self, resource_id: str) -> None:
        """
        Delete a resource by ID.

        Args:
            resource_id: Resource identifier

        Raises:
            ResourceNotFoundError: If resource not found
        """
        self.logger.info(f"Deleting resource: {resource_id}")

        if resource_id not in self._resources:
            error = ResourceNotFoundError(
                f"Resource with ID '{resource_id}' not found",
                {'resource_id': resource_id}
            )
            self.error_handler.handle_error(error, reraise=True)

        del self._resources[resource_id]
        self.logger.info(f"Successfully deleted resource: {resource_id}")
