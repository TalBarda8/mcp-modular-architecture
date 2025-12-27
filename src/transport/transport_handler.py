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
        """Handle incoming transport message and route to appropriate handler.

        This is the main entry point for all transport-layer messages. Implements
        a routing dispatcher pattern that:
        1. Extracts method name and parameters from message
        2. Routes to appropriate handler based on method
        3. Wraps result in success/error response format
        4. Provides comprehensive error handling and logging

        Args:
            message: JSON-RPC style message dictionary with structure:
                {
                    "method": str,  # e.g., "tool.execute", "server.info"
                    "params": dict,  # Optional parameters (default: {})
                    "id": Any  # Optional request ID for correlation
                }

        Returns:
            Response dictionary with structure:
                Success: {"success": True, "result": <data>, "id": <request_id>}
                Error: {"success": False, "error": {"code": str, "message": str}, "id": <request_id>}

        Supported Methods:
            - server.info: Get server metadata
            - server.initialize: Initialize server
            - tool.execute: Execute a registered tool
            - tool.list: List available tools
            - resource.read: Read a resource by URI
            - resource.list: List available resources
            - prompt.get_messages: Get prompt messages
            - prompt.list: List available prompts

        Error Conditions:
            - Unknown method: Returns method_not_found error
            - Missing required params: Handler raises ValueError, caught as internal_error
            - Handler exception: Any exception caught and logged, returned as internal_error
            - Malformed message: Caught by try-except, returned as internal_error

        Architectural Role:
            Acts as Adapter pattern between transport layer (STDIO, HTTP, etc.)
            and MCP server. Decouples transport protocol from server implementation,
            allowing transport to be swapped without changing server code.

        Notes:
            - All errors are caught and returned as error responses (never raises)
            - Logs all requests and errors for observability
            - Request ID preserved in response for correlation
            - Handler methods delegate to MessageHandlers helper class
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
