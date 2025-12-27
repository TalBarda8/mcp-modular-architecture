"""Base command handler with common functionality."""

import sys
from typing import Callable


class BaseCommand:
    """Base class for CLI command handlers."""

    def __init__(self, client_factory: Callable, logger):
        """
        Initialize command handler.

        Args:
            client_factory: Callable that creates MCPClient instances
            logger: Logger instance
        """
        self.create_client = client_factory
        self.logger = logger

    def handle_error(self, error: Exception, context: str) -> int:
        """
        Handle command error.

        Args:
            error: Exception that occurred
            context: Error context description

        Returns:
            Exit code 1
        """
        print(f"Error: {error}", file=sys.stderr)
        self.logger.error(f"{context}: {error}")
        return 1
