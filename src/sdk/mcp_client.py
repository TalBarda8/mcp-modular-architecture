"""
MCP Client SDK.

Provides a high-level interface for interacting with MCP servers.
Wraps transport communication and exposes simple methods for
tools, resources, and prompts.
"""

from typing import Any, Dict, List, Optional

from src.core.logging.logger import Logger
from src.core.errors.error_handler import ErrorHandler
from src.transport.base_transport import BaseTransport
from src.sdk.mcp_client_operations import ClientOperations


class MCPClient:
    """
    MCP Client SDK.

    Thin wrapper around transport layer that provides high-level
    methods for interacting with MCP server capabilities.

    The client is transport-agnostic and works with any transport
    implementation (STDIO, HTTP, SSE, etc.).
    """

    def __init__(self, transport: BaseTransport):
        """
        Initialize MCP client.

        Args:
            transport: Transport instance to use for communication
        """
        self.transport = transport
        self.logger = Logger.get_logger("MCPClient")
        self.error_handler = ErrorHandler("MCPClient")
        self._request_id = 0
        self._operations = ClientOperations(self._send_request)

    def _next_request_id(self) -> str:
        """
        Generate next request ID.

        Returns:
            Unique request ID string
        """
        self._request_id += 1
        return f"req-{self._request_id}"

    def _send_request(
        self,
        method: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send a request and wait for response.

        Args:
            method: Method name (e.g., 'server.info', 'tool.execute')
            params: Optional parameters dictionary

        Returns:
            Response dictionary

        Raises:
            Exception: If request fails or response indicates error
        """
        request = {
            "method": method,
            "id": self._next_request_id()
        }

        if params:
            request["params"] = params

        self.logger.debug(f"Sending request: {method}")

        # Send request
        self.transport.send_message(request)

        # Receive response
        response = self.transport.receive_message()

        if not response:
            raise Exception("No response received from server")

        # Check for error
        if not response.get("success", False):
            error = response.get("error", {})
            error_msg = error.get("message", "Unknown error") if isinstance(error, dict) else str(error)
            raise Exception(f"Server error: {error_msg}")

        return response.get("result", {})

    def connect(self) -> None:
        """Connect to the MCP server."""
        self.logger.info("Connecting to MCP server")
        self.transport.start()

    def disconnect(self) -> None:
        """Disconnect from the MCP server."""
        self.logger.info("Disconnecting from MCP server")
        self.transport.stop()

    def get_server_info(self) -> Dict[str, Any]:
        """Get server information."""
        return self._send_request("server.info")

    def initialize_server(self) -> Dict[str, Any]:
        """Initialize the server."""
        return self._send_request("server.initialize")

    def list_tools(self) -> List[str]:
        """List available tools."""
        return self._operations.list_tools()

    def execute_tool(
        self, tool_name: str, parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a tool."""
        return self._operations.execute_tool(tool_name, parameters)

    def list_resources(self) -> List[str]:
        """List available resources."""
        return self._operations.list_resources()

    def read_resource(self, uri: str) -> Dict[str, Any]:
        """Read a resource."""
        return self._operations.read_resource(uri)

    def list_prompts(self) -> List[str]:
        """List available prompts."""
        return self._operations.list_prompts()

    def get_prompt_messages(
        self, prompt_name: str, arguments: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, str]]:
        """Get prompt messages."""
        return self._operations.get_prompt_messages(prompt_name, arguments)

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
        return False
