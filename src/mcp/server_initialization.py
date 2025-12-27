"""
MCP Server Initialization.

Handles server lifecycle operations including startup and shutdown.
"""

from typing import List, Optional

from src.mcp.tools.base_tool import BaseTool
from src.mcp.resources.base_resource import BaseResource
from src.mcp.prompts.base_prompt import BasePrompt


class ServerInitialization:
    """MCP Server initialization and lifecycle management."""

    def __init__(self, server):
        """
        Initialize server lifecycle manager.

        Args:
            server: MCPServer instance
        """
        self.server = server
        self.logger = server.logger
        self.config = server.config
        self.error_handler = server.error_handler
        self.tool_registry = server.tool_registry
        self.resource_registry = server.resource_registry
        self.prompt_registry = server.prompt_registry

    def initialize(
        self,
        tools: Optional[List[BaseTool]] = None,
        resources: Optional[List[BaseResource]] = None,
        prompts: Optional[List[BasePrompt]] = None
    ) -> None:
        """
        Initialize the MCP server.

        Args:
            tools: Optional list of tools to register at startup
            resources: Optional list of resources to register at startup
            prompts: Optional list of prompts to register at startup
        """
        if self.server._initialized:
            self.logger.warning("Server already initialized")
            return

        self.logger.info("Initializing MCP Server")

        # Get server configuration
        server_name = self.config.get('mcp.server.name', 'MCP Server')
        server_version = self.config.get('mcp.server.version', '1.0.0')

        self.logger.info(f"Server: {server_name} v{server_version}")

        # Register provided tools
        if tools:
            for tool in tools:
                try:
                    self.tool_registry.register(tool)
                except Exception as e:
                    self.error_handler.handle_error(
                        e,
                        context={'tool': tool.name}
                    )

        # Register provided resources
        if resources:
            for resource in resources:
                try:
                    self.resource_registry.register(resource)
                except Exception as e:
                    self.error_handler.handle_error(
                        e,
                        context={'resource': resource.uri}
                    )

        # Register provided prompts
        if prompts:
            for prompt in prompts:
                try:
                    self.prompt_registry.register(prompt)
                except Exception as e:
                    self.error_handler.handle_error(
                        e,
                        context={'prompt': prompt.name}
                    )

        self.server._initialized = True
        self.logger.info(
            f"MCP Server initialized with {len(self.tool_registry)} tools, "
            f"{len(self.resource_registry)} resources, "
            f"{len(self.prompt_registry)} prompts"
        )

    def shutdown(self) -> None:
        """Shutdown the MCP server."""
        if not self.server._initialized:
            self.logger.warning("Server not initialized, nothing to shutdown")
            return

        self.logger.info("Shutting down MCP Server")

        # Clear all registries
        tool_count = len(self.tool_registry)
        resource_count = len(self.resource_registry)
        prompt_count = len(self.prompt_registry)

        self.tool_registry.clear()
        self.resource_registry.clear()
        self.prompt_registry.clear()

        self.server._initialized = False
        self.logger.info(
            f"MCP Server shutdown ({tool_count} tools, "
            f"{resource_count} resources, {prompt_count} prompts cleared)"
        )
