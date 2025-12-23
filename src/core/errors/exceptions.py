"""
Custom exception classes for the application.
Provides a hierarchy of exceptions for different error scenarios.
"""

from typing import Optional


class BaseApplicationError(Exception):
    """
    Base exception class for all application errors.

    All custom exceptions should inherit from this class.
    """

    def __init__(self, message: str, details: Optional[dict] = None):
        """
        Initialize the exception.

        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        """Return string representation of the error."""
        if self.details:
            return f"{self.message} (details: {self.details})"
        return self.message


class ConfigurationError(BaseApplicationError):
    """Raised when there's a configuration-related error."""
    pass


class ValidationError(BaseApplicationError):
    """Raised when data validation fails."""
    pass


class ServiceError(BaseApplicationError):
    """Raised when a service operation fails."""
    pass


class ResourceNotFoundError(BaseApplicationError):
    """Raised when a requested resource is not found."""
    pass


class ResourceAlreadyExistsError(BaseApplicationError):
    """Raised when attempting to create a resource that already exists."""
    pass
