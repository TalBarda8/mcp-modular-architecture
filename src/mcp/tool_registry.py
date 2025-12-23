"""
Tool Registry for managing MCP tools.
Provides centralized registration and discovery of available tools.
"""

from typing import Dict, List, Optional

from src.mcp.tools.base_tool import BaseTool
from src.core.logging.logger import Logger
from src.core.errors.exceptions import (
    ResourceAlreadyExistsError,
    ResourceNotFoundError
)


class ToolRegistry:
    """
    Registry for managing available MCP tools.

    Provides:
    - Tool registration and unregistration
    - Tool discovery by name
    - Listing all available tools
    - Tool metadata access

    Implements singleton pattern to ensure single source of truth.
    """

    _instance: Optional['ToolRegistry'] = None
    _tools: Dict[str, BaseTool] = {}

    def __new__(cls) -> 'ToolRegistry':
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the tool registry."""
        self.logger = Logger.get_logger(__name__)

    def register(self, tool: BaseTool) -> None:
        """
        Register a tool in the registry.

        Args:
            tool: Tool instance to register

        Raises:
            ResourceAlreadyExistsError: If tool with same name exists
        """
        tool_name = tool.name

        if tool_name in self._tools:
            raise ResourceAlreadyExistsError(
                f"Tool '{tool_name}' is already registered",
                {'tool_name': tool_name}
            )

        self._tools[tool_name] = tool
        self.logger.info(f"Registered tool: {tool_name}")

    def unregister(self, tool_name: str) -> None:
        """
        Unregister a tool from the registry.

        Args:
            tool_name: Name of tool to unregister

        Raises:
            ResourceNotFoundError: If tool not found
        """
        if tool_name not in self._tools:
            raise ResourceNotFoundError(
                f"Tool '{tool_name}' not found in registry",
                {'tool_name': tool_name}
            )

        del self._tools[tool_name]
        self.logger.info(f"Unregistered tool: {tool_name}")

    def get_tool(self, tool_name: str) -> BaseTool:
        """
        Get a tool by name.

        Args:
            tool_name: Name of the tool

        Returns:
            Tool instance

        Raises:
            ResourceNotFoundError: If tool not found
        """
        if tool_name not in self._tools:
            raise ResourceNotFoundError(
                f"Tool '{tool_name}' not found in registry",
                {'tool_name': tool_name}
            )

        return self._tools[tool_name]

    def list_tools(self) -> List[str]:
        """
        List all registered tool names.

        Returns:
            List of tool names
        """
        return list(self._tools.keys())

    def get_tools_metadata(self) -> List[Dict]:
        """
        Get metadata for all registered tools.

        Returns:
            List of tool metadata dictionaries
        """
        return [tool.to_dict() for tool in self._tools.values()]

    def clear(self) -> None:
        """
        Clear all registered tools.

        Useful for testing and cleanup.
        """
        self._tools.clear()
        self.logger.info("Cleared all tools from registry")

    def __len__(self) -> int:
        """Return the number of registered tools."""
        return len(self._tools)

    def __contains__(self, tool_name: str) -> bool:
        """Check if a tool is registered."""
        return tool_name in self._tools
