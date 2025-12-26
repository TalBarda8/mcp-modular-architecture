"""
UI Package.

Provides user interface implementations for interacting with MCP servers.
All UI implementations use the MCP Client SDK.
"""

from src.ui.cli import MCPCLI

__all__ = [
    "MCPCLI",
]
