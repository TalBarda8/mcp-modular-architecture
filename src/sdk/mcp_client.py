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
        """Initialize MCP client with transport layer.

        Creates a transport-agnostic client that wraps low-level transport
        communication with a high-level API. The client uses composition to
        delegate operation methods (tools, resources, prompts) to ClientOperations
        helper while managing transport lifecycle and request/response handling.

        Args:
            transport: BaseTransport implementation (e.g., STDIOTransport, HTTPTransport).
                Must implement send_message() and receive_message() methods.

        Architectural Role:
            Implements Facade pattern, providing simple SDK methods that hide
            transport complexity. Enables transport swapping without changing
            client code (Dependency Inversion Principle).

        Notes:
            - Transport must be started via connect() before sending requests
            - Use as context manager (with statement) for automatic lifecycle management
            - Request IDs auto-increment to enable request/response correlation
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
        """Send request via transport and wait for response.

        Core transport handling method that:
        1. Constructs JSON-RPC style request with unique ID
        2. Sends request through transport layer
        3. Blocks waiting for response (synchronous)
        4. Validates response and extracts result
        5. Converts server errors to exceptions

        Args:
            method: RPC method name following MCP protocol conventions
                (e.g., 'server.info', 'tool.execute', 'resource.read')
            params: Optional method-specific parameters as dictionary.
                Must match server-side expectations for the method.

        Returns:
            Result dictionary extracted from successful response.
            Structure varies by method (e.g., tool execution returns tool output,
            server.info returns server metadata).

        Raises:
            Exception: If no response received from server (timeout or connection failure)
            Exception: If server returns error response (with "Server error: " prefix)

        Error Conditions:
            - Transport send failure: Underlying transport exception propagated
            - No response: Raises "No response received from server"
            - Server error response: Extracts error message and raises with "Server error:" prefix
            - Malformed response: Missing 'result' returns empty dict {}

        Transport Protocol:
            Request format:  {"method": str, "id": str, "params": dict (optional)}
            Response format: {"success": bool, "result": dict | "error": dict, "id": str}

        Notes:
            - Blocking/synchronous operation (waits for complete response)
            - Request IDs ensure response correlation (not validated here)
            - Used by all high-level SDK methods (execute_tool, read_resource, etc.)
            - Errors are raised (not returned), caught by calling code
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
        """Context manager entry - establish connection.

        Enables 'with' statement usage for automatic connection lifecycle:
            with MCPClient(transport) as client:
                client.execute_tool(...)  # Connection automatically managed

        Returns:
            self: Client instance for use within 'with' block

        Notes:
            - Calls connect() to start transport layer
            - Connection remains open until __exit__
            - Use for scripts/tests to ensure cleanup
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - clean up connection.

        Automatically called when exiting 'with' block, ensuring transport
        cleanup even if exceptions occur within the block.

        Args:
            exc_type: Exception type if exception occurred (or None)
            exc_val: Exception value if exception occurred (or None)
            exc_tb: Exception traceback if exception occurred (or None)

        Returns:
            False: Exceptions are not suppressed (propagate to caller)

        Notes:
            - Calls disconnect() to stop transport layer
            - Always executes (even on exceptions in 'with' block)
            - Returning False allows exceptions to propagate naturally
        """
        self.disconnect()
        return False
