"""
Transport Handler.

Bridges the transport layer with the MCP server using routing table pattern.
Handles message routing and protocol translation.

Supported Methods:
- server.info: Get server metadata
- server.initialize: Initialize server
- tool.execute: Execute a registered tool
- tool.list: List available tools
- resource.read: Read a resource by URI
- resource.list: List available resources
- prompt.get_messages: Get prompt messages
- prompt.list: List available prompts
"""

from typing import Any, Dict, Callable

from src.core.logging.logger import Logger
from src.core.errors.error_handler import ErrorHandler
from src.mcp.server import MCPServer
from src.transport.transport_message_handlers import MessageHandlers


class TransportHandler:
    """
    Transport handler for MCP server.

    Acts as an adapter between the transport layer and the MCP server,
    keeping them completely decoupled.
    """

    def __init__(self, server: MCPServer):
        """Initialize transport handler with MCP server."""
        self.server = server
        self.logger = Logger.get_logger("TransportHandler")
        self.error_handler = ErrorHandler("TransportHandler")
        self.handlers = MessageHandlers(server)
        self._route_table = self._build_route_table()

    def _build_route_table(self) -> Dict[str, Callable]:
        """Build method routing table."""
        return {
            "server.info": self.handlers.handle_server_info,
            "server.initialize": self.handlers.handle_server_initialize,
            "tool.execute": self.handlers.handle_tool_execute,
            "tool.list": self.handlers.handle_tool_list,
            "resource.read": self.handlers.handle_resource_read,
            "resource.list": self.handlers.handle_resource_list,
            "prompt.get_messages": self.handlers.handle_prompt_get_messages,
            "prompt.list": self.handlers.handle_prompt_list,
        }

    def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming transport message and route to appropriate handler.

        Args:
            message: JSON-RPC style message with 'method', 'params', 'id'

        Returns:
            Response dictionary with 'success', 'result'/'error', 'id'
        """
        try:
            method = message.get("method")
            params = message.get("params", {})
            request_id = message.get("id")

            self.logger.info(f"Handling request: {method}")

            # Route using table lookup
            handler = self._route_table.get(method)
            if not handler:
                return self._error_response(
                    f"Unknown method: {method}",
                    "method_not_found",
                    request_id
                )

            # Execute handler (with or without params)
            if method in ["server.info", "tool.list", "resource.list", "prompt.list"]:
                result = handler()
            else:
                result = handler(params)

            return self._success_response(result, request_id)

        except Exception as e:
            self.logger.error(f"Error handling message: {str(e)}")
            self.error_handler.handle_error(e, context={'message': message})
            return self._error_response(
                str(e),
                "internal_error",
                message.get("id")
            )

    def _success_response(
        self, result: Any, request_id: Any = None
    ) -> Dict[str, Any]:
        """Create a success response."""
        response = {"success": True, "result": result}
        if request_id is not None:
            response["id"] = request_id
        return response

    def _error_response(
        self,
        message: str,
        code: str = "internal_error",
        request_id: Any = None
    ) -> Dict[str, Any]:
        """Create an error response."""
        response = {
            "success": False,
            "error": {"code": code, "message": message}
        }
        if request_id is not None:
            response["id"] = request_id
        return response
