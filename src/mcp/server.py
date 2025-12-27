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
        """Initialize the MCP server.

        Creates a new MCP server instance with orchestration components for
        initialization, operations, and registry management. This constructor
        sets up the foundational infrastructure (config, logging, error handling)
        and three singleton registries for tools, resources, and prompts.

        Architectural Role:
            This is the main orchestration point where all server subsystems are
            instantiated and wired together using composition pattern. The server
            delegates to helper classes (ServerInitialization, ServerOperations,
            ServerRegistry) to maintain single responsibility principle.

        Raises:
            ConfigurationError: If configuration files are malformed
            ServiceError: If singleton registries fail to initialize

        Notes:
            - Server starts in uninitialized state (_initialized=False)
            - Must call initialize() before using tool/resource/prompt operations
            - All registries use singleton pattern (shared across server instances)
        """
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
        """Initialize the MCP server and register provided components.

        Orchestrates server initialization by delegating to ServerInitialization
        helper. This method registers provided tools/resources/prompts and marks
        the server as ready for operation. Idempotent - calling multiple times
        logs a warning and returns early.

        Args:
            tools: Optional list of BaseTool instances to register at startup.
                Each tool must implement _define_schema() and _execute_impl().
            resources: Optional list of BaseResource instances to register.
                Can be static (file-based) or dynamic (computed).
            prompts: Optional list of BasePrompt instances to register.
                Each prompt defines message templates with argument substitution.

        Raises:
            ValidationError: If any tool/resource/prompt fails schema validation
            ResourceAlreadyExistsError: If attempting to register duplicate names

        Notes:
            - Registration errors are caught and logged but don't halt initialization
            - Server becomes operational (_initialized=True) even if some
              components fail to register
            - Use register_tool/resource/prompt() methods to add components
              dynamically after initialization
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
        """Execute a registered tool with given parameters.

        Orchestrates tool execution by delegating to ServerOperations helper,
        which handles tool lookup, validation, execution, and error handling.

        Args:
            tool_name: Name of the registered tool to execute (e.g., 'calculator')
            params: Dictionary of parameters matching the tool's input schema

        Returns:
            Dictionary containing execution result with structure:
                {'success': True, 'result': <tool_output>} on success
                {'success': False, 'error': <error_message>} on failure

        Error Conditions:
            - Server not initialized: Returns {'success': False, 'error': 'Server not initialized'}
            - Tool not found: Caught by ServerOperations, returns error dict
            - Validation failure: Invalid params caught, returns error dict
            - Execution exception: Any runtime error caught and logged

        Notes:
            - All errors are gracefully handled and returned as error dicts
            - Never raises exceptions to caller (error-safe API)
            - Execution is synchronous (blocks until tool completes)
        """
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
        """Get comprehensive server metadata and status.

        Aggregates information from multiple sources (configuration, registries,
        initialization state) to provide a complete server status snapshot.

        Returns:
            Dictionary with server metadata containing:
                - name: Server name from config (default: 'MCP Server')
                - version: Server version from config (default: '1.0.0')
                - description: Human-readable description
                - initialized: Boolean indicating if initialize() was called
                - tool_count: Number of registered tools
                - resource_count: Number of registered resources
                - prompt_count: Number of registered prompts
                - capabilities: Dict of supported MCP primitives (all True)

        Notes:
            - Safe to call before initialization (returns partial info)
            - Counts reflect current registry state (may change dynamically)
            - Used by transport layer for 'server.info' method
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
