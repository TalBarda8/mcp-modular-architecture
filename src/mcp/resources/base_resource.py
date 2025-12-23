"""
Base abstraction for MCP Resources.
Resources are read-only data sources (static or dynamic).
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from src.core.logging.logger import Logger
from src.core.errors.error_handler import ErrorHandler


class BaseResource(ABC):
    """
    Abstract base class for all MCP resources.

    Resources provide read-only access to data (static or dynamic).
    All concrete resources must inherit from this class.
    """

    def __init__(self, uri: str, name: str, description: str, mime_type: str = "text/plain"):
        """
        Initialize the base resource.

        Args:
            uri: Unique resource identifier (URI format)
            name: Human-readable resource name
            description: Resource description
            mime_type: MIME type of the resource content
        """
        self.uri = uri
        self.name = name
        self.description = description
        self.mime_type = mime_type
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.error_handler = ErrorHandler(self.__class__.__name__)

    @abstractmethod
    def read(self) -> Dict[str, Any]:
        """
        Read the resource content.

        Must be implemented by concrete resources.

        Returns:
            Dictionary containing resource content and metadata

        Raises:
            Various exceptions based on resource type
        """
        pass

    @abstractmethod
    def is_dynamic(self) -> bool:
        """
        Check if resource is dynamic (content changes over time).

        Returns:
            True if dynamic, False if static
        """
        pass

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get resource metadata.

        Returns:
            Dictionary containing resource metadata
        """
        return {
            'uri': self.uri,
            'name': self.name,
            'description': self.description,
            'mimeType': self.mime_type,
            'isDynamic': self.is_dynamic()
        }

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert resource to dictionary representation.

        Returns:
            Dictionary containing full resource information
        """
        return self.get_metadata()

    def __repr__(self) -> str:
        """Return string representation of the resource."""
        resource_type = "dynamic" if self.is_dynamic() else "static"
        return f"{self.__class__.__name__}(uri={self.uri}, type={resource_type})"
