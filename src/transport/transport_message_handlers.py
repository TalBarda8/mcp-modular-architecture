"""
Transport Message Handlers.

Individual handler methods for different MCP message types.
"""

from typing import Any, Dict


class MessageHandlers:
    """Message handlers for MCP protocol methods."""

    def __init__(self, server):
        """
        Initialize message handlers.

        Args:
            server: MCPServer instance
        """
        self.server = server

    def handle_server_info(self) -> Dict[str, Any]:
        """Handle server.info request."""
        return self.server.get_info()

    def handle_server_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle server.initialize request."""
        self.server.initialize()
        return {"status": "initialized"}

    def handle_tool_execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool.execute request."""
        tool_name = params.get("name")
        tool_params = params.get("parameters", {})

        if not tool_name:
            raise ValueError("Tool name is required")

        return self.server.execute_tool(tool_name, tool_params)

    def handle_tool_list(self) -> Dict[str, Any]:
        """Handle tool.list request."""
        tools = self.server.list_tools()
        return {"tools": tools}

    def handle_resource_read(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle resource.read request."""
        uri = params.get("uri")

        if not uri:
            raise ValueError("Resource URI is required")

        return self.server.read_resource(uri)

    def handle_resource_list(self) -> Dict[str, Any]:
        """Handle resource.list request."""
        resources = self.server.list_resources()
        return {"resources": resources}

    def handle_prompt_get_messages(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle prompt.get_messages request."""
        name = params.get("name")
        arguments = params.get("arguments", {})

        if not name:
            raise ValueError("Prompt name is required")

        return self.server.get_prompt_messages(name, arguments)

    def handle_prompt_list(self) -> Dict[str, Any]:
        """Handle prompt.list request."""
        prompts = self.server.list_prompts()
        return {"prompts": prompts}
