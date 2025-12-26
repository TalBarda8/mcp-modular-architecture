"""
Example resource model demonstrating OOP principles.
This is a simple domain model for demonstration purposes.
"""

from typing import Any, Dict, Optional
from src.models.base_model import BaseModel
from src.core.errors.exceptions import ValidationError


class Resource(BaseModel):
    """
    Example resource model.

    Represents a generic resource with an ID, name, and status.
    Demonstrates validation and OOP principles.
    """

    def __init__(
        self,
        resource_id: str,
        name: str,
        status: str = 'active',
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a resource.

        Args:
            resource_id: Unique identifier for the resource
            name: Resource name
            status: Resource status (active, inactive, pending)
            metadata: Additional metadata dictionary
        """
        super().__init__()
        self.resource_id = resource_id
        self.name = name
        self.status = status
        self.metadata = metadata or {}
        self.validate()

    def validate(self) -> bool:
        """
        Validate the resource data.

        Returns:
            True if validation passes

        Raises:
            ValidationError: If validation fails
        """
        if not self.resource_id or not isinstance(self.resource_id, str):
            raise ValidationError(
                "resource_id must be a non-empty string",
                {'resource_id': self.resource_id}
            )

        if not self.name or not isinstance(self.name, str):
            raise ValidationError(
                "name must be a non-empty string",
                {'name': self.name}
            )

        valid_statuses = ['active', 'inactive', 'pending']
        if self.status not in valid_statuses:
            raise ValidationError(
                f"status must be one of {valid_statuses}",
                {'status': self.status}
            )

        return True

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert resource to dictionary representation.

        Returns:
            Dictionary representation of the resource
        """
        data = super().to_dict()
        data.update({
            'resource_id': self.resource_id,
            'name': self.name,
            'status': self.status,
            'metadata': self.metadata
        })
        return data

    def activate(self) -> None:
        """Activate the resource."""
        self.status = 'active'
        self.update_timestamp()

    def deactivate(self) -> None:
        """Deactivate the resource."""
        self.status = 'inactive'
        self.update_timestamp()

    def __repr__(self) -> str:
        """Return string representation of the resource."""
        return (
            f"Resource(id={self.resource_id}, "
            f"name={self.name}, status={self.status})"
        )
