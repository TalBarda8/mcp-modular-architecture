"""
Base model class providing common functionality.
All domain models should inherit from this class.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict


class BaseModel(ABC):
    """
    Abstract base class for all domain models.

    Provides common functionality like validation,
    serialization, and timestamp management.
    """

    def __init__(self):
        """Initialize the base model with timestamps."""
        self.created_at: datetime = datetime.now()
        self.updated_at: datetime = datetime.now()

    @abstractmethod
    def validate(self) -> bool:
        """
        Validate the model's data.

        Returns:
            True if validation passes

        Raises:
            ValidationError: If validation fails
        """
        pass

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model to dictionary representation.

        Returns:
            Dictionary representation of the model
        """
        return {
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def update_timestamp(self) -> None:
        """Update the model's updated_at timestamp."""
        self.updated_at = datetime.now()

    def __repr__(self) -> str:
        """Return string representation of the model."""
        return f"{self.__class__.__name__}(created_at={self.created_at})"
