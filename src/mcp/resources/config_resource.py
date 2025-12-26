"""
Configuration Resource - Example static resource.
Provides read-only access to configuration data.
"""

from typing import Any, Dict

from src.mcp.resources.base_resource import BaseResource
from src.core.config.config_manager import ConfigManager


class ConfigResource(BaseResource):
    """
    Static resource providing access to application configuration.

    Demonstrates:
    - Static resource (content doesn't change during runtime)
    - Integration with core infrastructure (ConfigManager)
    - Read-only data access pattern

    Note: This is an illustrative example demonstrating architecture.
    """

    def __init__(self):
        """Initialize the configuration resource."""
        super().__init__(
            uri="config://app",
            name="Application Configuration",
            description="Read-only access to application configuration",
            mime_type="application/json"
        )
        self.config = ConfigManager()

    def read(self) -> Dict[str, Any]:
        """
        Read the configuration data.

        Returns:
            Dictionary containing configuration content
        """
        self.logger.debug(f"Reading resource: {self.uri}")

        try:
            config_data = self.config.get_all()

            return {
                'uri': self.uri,
                'mimeType': self.mime_type,
                'content': config_data
            }

        except Exception as e:
            self.error_handler.handle_error(
                e,
                context={'resource': self.uri}
            )
            return {
                'uri': self.uri,
                'mimeType': self.mime_type,
                'content': {},
                'error': str(e)
            }

    def is_dynamic(self) -> bool:
        """
        Configuration is static (doesn't change during runtime).

        Returns:
            False - this is a static resource
        """
        return False
