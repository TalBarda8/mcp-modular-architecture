"""
MCP Server Bootstrap.
MCP server implementation supporting Tools, Resources, and Prompts.
"""

from typing import Any, Dict, List, Optional

from src.core.config.config_manager import ConfigManager
from src.core.logging.logger import Logger
from src.core.errors.error_handler import ErrorHandler
from src.mcp.tool_registry import ToolRegistry
from src.mcp.resource_registry import ResourceRegistry
from src.mcp.prompt_registry import PromptRegistry
from src.mcp.tools.base_tool import BaseTool
from src.mcp.resources.base_resource import BaseResource
from src.mcp.prompts.base_prompt import BasePrompt
from src.mcp.server_initialization import ServerInitialization
from src.mcp.server_operations import ServerOperations
from src.mcp.server_registry import ServerRegistry


class MCPServer:
    """
    MCP Server implementation.

    Provides:
    - Server initialization and configuration
    - Tool registration and management
    - Resource registration and access
    - Prompt registration and message generation
    - Server lifecycle management

    The server supports all three MCP primitives (tools, resources, prompts)
    and communicates via pluggable transport layers (STDIO, HTTP, WebSocket).
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

        # Initialize helper components
        self._initializer = ServerInitialization(self)
        self._operations = ServerOperations(self)
        self._registry = ServerRegistry(self)

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
        self._initializer.initialize(tools, resources, prompts)

    def register_tool(self, tool: BaseTool) -> None:
        """Register a tool with the server."""
        self._registry.register_tool(tool)

    def register_resource(self, resource: BaseResource) -> None:
        """Register a resource with the server."""
        self._registry.register_resource(resource)

    def register_prompt(self, prompt: BasePrompt) -> None:
        """Register a prompt with the server."""
        self._registry.register_prompt(prompt)

    def list_tools(self) -> List[str]:
        """List all registered tool names."""
        return self._registry.list_tools()

    def get_tools_metadata(self) -> List[Dict[str, Any]]:
        """Get metadata for all registered tools."""
        return self._registry.get_tools_metadata()

    def list_resources(self) -> List[str]:
        """List all registered resource URIs."""
        return self._registry.list_resources()

    def get_resources_metadata(self) -> List[Dict[str, Any]]:
        """Get metadata for all registered resources."""
        return self._registry.get_resources_metadata()

    def list_prompts(self) -> List[str]:
        """List all registered prompt names."""
        return self._registry.list_prompts()

    def get_prompts_metadata(self) -> List[Dict[str, Any]]:
        """Get metadata for all registered prompts."""
        return self._registry.get_prompts_metadata()

    def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool by name with given parameters."""
        return self._operations.execute_tool(tool_name, params)

    def read_resource(self, resource_uri: str) -> Dict[str, Any]:
        """Read a resource by URI."""
        return self._operations.read_resource(resource_uri)

    def get_prompt_messages(
        self, prompt_name: str, arguments: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Get prompt messages with given arguments."""
        return self._operations.get_prompt_messages(prompt_name, arguments)

    def shutdown(self) -> None:
        """Shutdown the MCP server."""
        self._initializer.shutdown()

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
            'description': 'MCP server with tools, resources, and prompts',
            'initialized': self._initialized,
            'tool_count': len(self.tool_registry),
            'resource_count': len(self.resource_registry),
            'prompt_count': len(self.prompt_registry),
            'capabilities': {
                'tools': True,
                'resources': True,
                'prompts': True
            }
        }
