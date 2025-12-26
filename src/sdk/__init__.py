"""
SDK Package.

Provides a thin client SDK for interacting with MCP servers.
The SDK wraps transport communication and exposes high-level
methods for tools, resources, and prompts.
"""

from src.sdk.mcp_client import MCPClient

__all__ = [
    "MCPClient",
]
