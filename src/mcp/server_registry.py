"""
MCP Server Registry Management.

Handles component registration and metadata retrieval.
"""

from typing import Any, Dict, List

from src.core.errors.exceptions import ServiceError
from src.mcp.tools.base_tool import BaseTool
from src.mcp.resources.base_resource import BaseResource
from src.mcp.prompts.base_prompt import BasePrompt


class ServerRegistry:
    """MCP Server registry operations."""

    def __init__(self, server):
        """
        Initialize server registry manager.

        Args:
            server: MCPServer instance
        """
        self.server = server
        self.tool_registry = server.tool_registry
        self.resource_registry = server.resource_registry
        self.prompt_registry = server.prompt_registry

    def register_tool(self, tool: BaseTool) -> None:
        """
        Register a tool with the server.

        Args:
            tool: Tool instance to register
        """
        if not self.server._initialized:
            raise ServiceError(
                "Server not initialized. Call initialize() first.",
                {'server_initialized': False}
            )
        self.tool_registry.register(tool)

    def register_resource(self, resource: BaseResource) -> None:
        """
        Register a resource with the server.

        Args:
            resource: Resource instance to register
        """
        if not self.server._initialized:
            raise ServiceError(
                "Server not initialized. Call initialize() first.",
                {'server_initialized': False}
            )
        self.resource_registry.register(resource)

    def register_prompt(self, prompt: BasePrompt) -> None:
        """
        Register a prompt with the server.

        Args:
            prompt: Prompt instance to register
        """
        if not self.server._initialized:
            raise ServiceError(
                "Server not initialized. Call initialize() first.",
                {'server_initialized': False}
            )
        self.prompt_registry.register(prompt)

    def list_tools(self) -> List[str]:
        """
        List all registered tool names.

        Returns:
            List of tool names
        """
        return self.tool_registry.list_tools()

    def get_tools_metadata(self) -> List[Dict[str, Any]]:
        """
        Get metadata for all registered tools.

        Returns:
            List of tool metadata dictionaries
        """
        return self.tool_registry.get_tools_metadata()

    def list_resources(self) -> List[str]:
        """
        List all registered resource URIs.

        Returns:
            List of resource URIs
        """
        return self.resource_registry.list_resources()

    def get_resources_metadata(self) -> List[Dict[str, Any]]:
        """
        Get metadata for all registered resources.

        Returns:
            List of resource metadata dictionaries
        """
        return self.resource_registry.get_resources_metadata()

    def list_prompts(self) -> List[str]:
        """
        List all registered prompt names.

        Returns:
            List of prompt names
        """
        return self.prompt_registry.list_prompts()

    def get_prompts_metadata(self) -> List[Dict[str, Any]]:
        """
        Get metadata for all registered prompts.

        Returns:
            List of prompt metadata dictionaries
        """
        return self.prompt_registry.get_prompts_metadata()
