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
        """
        Connect to the MCP server.

        Starts the transport layer.
        """
        self.logger.info("Connecting to MCP server")
        self.transport.start()

    def disconnect(self) -> None:
        """
        Disconnect from the MCP server.

        Stops the transport layer.
        """
        self.logger.info("Disconnecting from MCP server")
        self.transport.stop()

    def get_server_info(self) -> Dict[str, Any]:
        """
        Get server information.

        Returns:
            Server information dictionary with name, version, capabilities, etc.
        """
        return self._send_request("server.info")

    def initialize_server(self) -> Dict[str, Any]:
        """
        Initialize the server.

        Returns:
            Initialization result
        """
        return self._send_request("server.initialize")

    # ===== Tool Methods =====

    def list_tools(self) -> List[str]:
        """
        List available tools.

        Returns:
            List of tool names
        """
        result = self._send_request("tool.list")
        return result.get("tools", [])

    def execute_tool(
        self,
        tool_name: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute a tool.

        Args:
            tool_name: Name of the tool to execute
            parameters: Tool parameters

        Returns:
            Tool execution result
        """
        params = {
            "name": tool_name,
            "parameters": parameters or {}
        }
        return self._send_request("tool.execute", params)

    # ===== Resource Methods =====

    def list_resources(self) -> List[str]:
        """
        List available resources.

        Returns:
            List of resource URIs
        """
        result = self._send_request("resource.list")
        return result.get("resources", [])

    def read_resource(self, uri: str) -> Dict[str, Any]:
        """
        Read a resource.

        Args:
            uri: Resource URI

        Returns:
            Resource content and metadata
        """
        params = {"uri": uri}
        return self._send_request("resource.read", params)

    # ===== Prompt Methods =====

    def list_prompts(self) -> List[str]:
        """
        List available prompts.

        Returns:
            List of prompt names
        """
        result = self._send_request("prompt.list")
        return result.get("prompts", [])

    def get_prompt_messages(
        self,
        prompt_name: str,
        arguments: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, str]]:
        """
        Get prompt messages.

        Args:
            prompt_name: Name of the prompt
            arguments: Prompt arguments

        Returns:
            List of message dictionaries with role and content
        """
        params = {
            "name": prompt_name,
            "arguments": arguments or {}
        }
        result = self._send_request("prompt.get_messages", params)
        return result.get("messages", [])

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
        return False
