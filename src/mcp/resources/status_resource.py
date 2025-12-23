"""
Status Resource - Example dynamic resource.
Provides real-time system status information.
"""

from datetime import datetime
from typing import Any, Dict

from src.mcp.resources.base_resource import BaseResource


class StatusResource(BaseResource):
    """
    Dynamic resource providing current system status.

    Demonstrates:
    - Dynamic resource (content changes each time it's read)
    - Real-time data access
    - Timestamp tracking

    Note: This is an illustrative example demonstrating architecture.
    """

    def __init__(self):
        """Initialize the status resource."""
        super().__init__(
            uri="status://system",
            name="System Status",
            description="Real-time system status information",
            mime_type="application/json"
        )
        self.read_count = 0

    def read(self) -> Dict[str, Any]:
        """
        Read current system status.

        Returns:
            Dictionary containing current status data
        """
        self.logger.debug(f"Reading resource: {self.uri}")

        try:
            self.read_count += 1

            status_data = {
                'timestamp': datetime.now().isoformat(),
                'status': 'operational',
                'read_count': self.read_count,
                'uptime_seconds': self._get_uptime()
            }

            return {
                'uri': self.uri,
                'mimeType': self.mime_type,
                'content': status_data
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
        Status is dynamic (changes with each read).

        Returns:
            True - this is a dynamic resource
        """
        return True

    def _get_uptime(self) -> int:
        """
        Get a simple uptime metric.

        Returns:
            Read count as proxy for uptime
        """
        # Simplified uptime - in real implementation would track actual uptime
        return self.read_count * 10
