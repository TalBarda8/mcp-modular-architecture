"""
UI Package.

Provides user interface implementations for interacting with MCP servers.
All UI implementations use the MCP Client SDK.

Note: UI code is excluded from unit test coverage (see pyproject.toml).
"""  # pragma: no cover

from src.ui.cli import MCPCLI

__all__ = [
    "MCPCLI",
]
