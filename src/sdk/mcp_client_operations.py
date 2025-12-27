"""
MCP Client API Operations.

Contains tool, resource, and prompt API methods.
"""

from typing import Any, Dict, List, Optional


class ClientOperations:
    """MCP Client API operations for tools, resources, and prompts."""

    def __init__(self, send_request_fn):
        """
        Initialize client operations.

        Args:
            send_request_fn: Function to send requests to server
        """
        self._send_request = send_request_fn

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
