"""
MCP Server Bootstrap.
MCP server implementation supporting Tools, Resources, and Prompts (Stage 3).
"""

from typing import Any, Dict, List, Optional

from src.core.config.config_manager import ConfigManager
from src.core.logging.logger import Logger
from src.core.errors.error_handler import ErrorHandler
from src.core.errors.exceptions import ServiceError
from src.mcp.tool_registry import ToolRegistry
from src.mcp.resource_registry import ResourceRegistry
from src.mcp.prompt_registry import PromptRegistry
from src.mcp.tools.base_tool import BaseTool
from src.mcp.resources.base_resource import BaseResource
from src.mcp.prompts.base_prompt import BasePrompt


class MCPServer:
    """
    MCP Server implementation for Stage 3.

    Provides:
    - Server initialization and configuration
    - Tool registration and management
    - Resource registration and access
    - Prompt registration and message generation
    - Server lifecycle management

    Note: This is Stage 3 - Tools, Resources, and Prompts.
    Transport layer (HTTP/SSE/STDIO) comes in Stage 4.
    """

    def __init__(self):
        """Initialize the MCP server."""
        self.config = ConfigManager()
        self.logger = Logger.get_logger(__name__)
        self.error_handler = ErrorHandler(__name__)
        self.tool_registry = ToolRegistry()
        self.resource_registry = ResourceRegistry()
        self.prompt_registry = PromptRegistry()
        self._initialized = False

        self.logger.info("MCP Server instance created")

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
        if self._initialized:
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

        self._initialized = True
        self.logger.info(
            f"MCP Server initialized with {len(self.tool_registry)} tools, "
            f"{len(self.resource_registry)} resources, "
            f"{len(self.prompt_registry)} prompts"
        )

    def register_tool(self, tool: BaseTool) -> None:
        """
        Register a tool with the server.

        Args:
            tool: Tool instance to register
        """
        if not self._initialized:
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
        if not self._initialized:
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
        if not self._initialized:
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

    def execute_tool(
        self,
        tool_name: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a tool by name with given parameters.

        Args:
            tool_name: Name of the tool to execute
            params: Tool input parameters

        Returns:
            Tool execution result
        """
        if not self._initialized:
            return {
                'success': False,
                'error': 'Server not initialized'
            }

        self.logger.info(f"Executing tool: {tool_name}")

        try:
            tool = self.tool_registry.get_tool(tool_name)
            result = tool.execute(params)
            return result

        except Exception as e:
            self.error_handler.handle_error(
                e,
                context={'tool_name': tool_name, 'params': params}
            )
            return {
                'success': False,
                'error': str(e)
            }

    def read_resource(self, resource_uri: str) -> Dict[str, Any]:
        """
        Read a resource by URI.

        Args:
            resource_uri: URI of the resource to read

        Returns:
            Resource content and metadata
        """
        if not self._initialized:
            return {
                'error': 'Server not initialized'
            }

        self.logger.info(f"Reading resource: {resource_uri}")

        try:
            resource = self.resource_registry.get_resource(resource_uri)
            content = resource.read()
            return content

        except Exception as e:
            self.error_handler.handle_error(
                e,
                context={'resource_uri': resource_uri}
            )
            return {
                'uri': resource_uri,
                'error': str(e)
            }

    def get_prompt_messages(
        self,
        prompt_name: str,
        arguments: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Get prompt messages with given arguments.

        Args:
            prompt_name: Name of the prompt
            arguments: Arguments for the prompt

        Returns:
            Dictionary containing messages or error
        """
        if not self._initialized:
            return {
                'success': False,
                'error': 'Server not initialized'
            }

        self.logger.info(f"Getting messages for prompt: {prompt_name}")

        try:
            prompt = self.prompt_registry.get_prompt(prompt_name)
            messages = prompt.get_messages(arguments)
            return {
                'success': True,
                'prompt': prompt_name,
                'messages': messages
            }

        except Exception as e:
            self.error_handler.handle_error(
                e,
                context={'prompt_name': prompt_name, 'arguments': arguments}
            )
            return {
                'success': False,
                'error': str(e)
            }

    def shutdown(self) -> None:
        """Shutdown the MCP server."""
        if not self._initialized:
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

        self._initialized = False
        self.logger.info(
            f"MCP Server shutdown ({tool_count} tools, "
            f"{resource_count} resources, {prompt_count} prompts cleared)"
        )

    @property
    def is_initialized(self) -> bool:
        """Check if server is initialized."""
        return self._initialized

    def get_info(self) -> Dict[str, Any]:
        """
        Get server information.

        Returns:
            Dictionary with server metadata
        """
        return {
            'name': self.config.get('mcp.server.name', 'MCP Server'),
            'version': self.config.get('mcp.server.version', '1.0.0'),
            'stage': 'Stage 3 - Tools, Resources, and Prompts',
            'initialized': self._initialized,
            'tool_count': len(self.tool_registry),
            'resource_count': len(self.resource_registry),
            'prompt_count': len(self.prompt_registry),
            'capabilities': {
                'tools': True,
                'resources': True,   # Stage 3
                'prompts': True      # Stage 3
            }
        }
