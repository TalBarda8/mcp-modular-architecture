"""
MCP Modular Architecture Reference Implementation.

A clean, layered architecture demonstrating professional software design principles:
- Core Infrastructure: Configuration, logging, and error handling
- MCP Server: Tools, resources, and prompts with registry pattern
- Transport Layer: Protocol-agnostic communication (STDIO, HTTP, WebSocket)
- SDK: High-level client library for MCP integration
- User Interface: CLI and other consumer interfaces
"""

__version__ = "1.0.0"

__all__ = [
    "__version__",
]
