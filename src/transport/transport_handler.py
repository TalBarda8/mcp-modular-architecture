"""
Transport Handler.

Bridges the transport layer with the MCP server.
Handles message routing and protocol translation.
"""

from typing import Any, Dict

from src.core.logging.logger import Logger
from src.core.errors.error_handler import ErrorHandler
from src.mcp.server import MCPServer
from src.transport.transport_message_handlers import MessageHandlers


class TransportHandler:
    """
    Transport handler for MCP server.

    Translates transport-level messages into MCP server operations
    and formats responses for transport transmission.

    This class acts as an adapter between the transport layer
    and the MCP server, keeping them completely decoupled.
    """

    def __init__(self, server: MCPServer):
        """
        Initialize transport handler.

        Args:
            server: MCP server instance to handle requests
        """
        self.server = server
        self.logger = Logger.get_logger("TransportHandler")
        self.error_handler = ErrorHandler("TransportHandler")
        self.handlers = MessageHandlers(server)

    def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle an incoming message.

        Args:
            message: Message to process

        Returns:
            Response dictionary

        Message format (JSON-RPC style):
        {
            "method": "tool.execute" | "resource.read" | "prompt.get_messages" | "server.info",
            "params": {...},
            "id": "request_id" (optional)
        }
        """
        try:
            method = message.get("method")
            params = message.get("params", {})
            request_id = message.get("id")

            self.logger.info(f"Handling request: {method}")

            # Route to appropriate handler
            if method == "server.info":
                result = self.handlers.handle_server_info()
            elif method == "server.initialize":
                result = self.handlers.handle_server_initialize(params)
            elif method == "tool.execute":
                result = self.handlers.handle_tool_execute(params)
            elif method == "tool.list":
                result = self.handlers.handle_tool_list()
            elif method == "resource.read":
                result = self.handlers.handle_resource_read(params)
            elif method == "resource.list":
                result = self.handlers.handle_resource_list()
            elif method == "prompt.get_messages":
                result = self.handlers.handle_prompt_get_messages(params)
            elif method == "prompt.list":
                result = self.handlers.handle_prompt_list()
            else:
                return self._error_response(
                    f"Unknown method: {method}",
                    "method_not_found",
                    request_id
                )

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
        """
        Create a success response.

        Args:
            result: Result data
            request_id: Request ID (optional)

        Returns:
            Success response dictionary
        """
        response = {
            "success": True,
            "result": result
        }

        if request_id is not None:
            response["id"] = request_id

        return response

    def _error_response(
        self,
        message: str,
        code: str = "internal_error",
        request_id: Any = None
    ) -> Dict[str, Any]:
        """
        Create an error response.

        Args:
            message: Error message
            code: Error code
            request_id: Request ID (optional)

        Returns:
            Error response dictionary
        """
        response = {
            "success": False,
            "error": {
                "code": code,
                "message": message
            }
        }

        if request_id is not None:
            response["id"] = request_id

        return response
