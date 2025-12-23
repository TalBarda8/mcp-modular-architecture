"""
MCP Server Bootstrap.
Minimal MCP server implementation for Stage 2 - focuses on tools only.
"""

from typing import Any, Dict, List, Optional

from src.core.config.config_manager import ConfigManager
from src.core.logging.logger import Logger
from src.core.errors.error_handler import ErrorHandler
from src.core.errors.exceptions import ServiceError
from src.mcp.tool_registry import ToolRegistry
from src.mcp.tools.base_tool import BaseTool


class MCPServer:
    """
    MCP Server implementation for Stage 2.

    Provides:
    - Server initialization and configuration
    - Tool registration and management
    - Tool execution interface
    - Server lifecycle management

    Note: This is Stage 2 - Tools only. No Resources, Prompts,
    or Transport layer yet (those come in later stages).
    """

    def __init__(self):
        """Initialize the MCP server."""
        self.config = ConfigManager()
        self.logger = Logger.get_logger(__name__)
        self.error_handler = ErrorHandler(__name__)
        self.tool_registry = ToolRegistry()
        self._initialized = False

        self.logger.info("MCP Server instance created")

    def initialize(self, tools: Optional[List[BaseTool]] = None) -> None:
        """
        Initialize the MCP server.

        Args:
            tools: Optional list of tools to register at startup
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

        self._initialized = True
        self.logger.info(
            f"MCP Server initialized with {len(self.tool_registry)} tools"
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

    def shutdown(self) -> None:
        """Shutdown the MCP server."""
        if not self._initialized:
            self.logger.warning("Server not initialized, nothing to shutdown")
            return

        self.logger.info("Shutting down MCP Server")

        # Clear tool registry
        tool_count = len(self.tool_registry)
        self.tool_registry.clear()

        self._initialized = False
        self.logger.info(f"MCP Server shutdown ({tool_count} tools cleared)")

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
            'stage': 'Stage 2 - Tools',
            'initialized': self._initialized,
            'tool_count': len(self.tool_registry),
            'capabilities': {
                'tools': True,
                'resources': False,  # Stage 3
                'prompts': False     # Stage 3
            }
        }
