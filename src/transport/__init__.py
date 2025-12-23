"""
Transport Layer Package.

Provides modular transport implementations for MCP server communication.
The transport layer is completely decoupled from MCP business logic,
allowing easy replacement of transport mechanisms.

Available transports:
- STDIO: Standard input/output (recommended for MCP)
- (Future: HTTP, SSE, WebSocket)
"""

from src.transport.base_transport import BaseTransport
from src.transport.stdio_transport import STDIOTransport
from src.transport.transport_handler import TransportHandler

__all__ = [
    "BaseTransport",
    "STDIOTransport",
    "TransportHandler",
]
