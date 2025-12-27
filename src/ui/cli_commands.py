"""
MCP CLI Command Dispatcher.

Delegates commands to specialized handlers organized by domain.
"""

from typing import Optional

from src.ui.commands import (
    ServerCommands,
    ToolCommands,
    ResourceCommands,
    PromptCommands
)


class CLICommands:
    """MCP CLI command dispatcher."""

    def __init__(self, client_factory, logger):
        """
        Initialize CLI command dispatcher.

        Args:
            client_factory: Callable that creates MCPClient instances
            logger: Logger instance
        """
        self.server_commands = ServerCommands(client_factory, logger)
        self.tool_commands = ToolCommands(client_factory, logger)
        self.resource_commands = ResourceCommands(client_factory, logger)
        self.prompt_commands = PromptCommands(client_factory, logger)

    def run_info(self) -> int:
        """Display server information."""
        return self.server_commands.run_info()

    def run_list_tools(self) -> int:
        """List available tools."""
        return self.tool_commands.run_list_tools()

    def run_execute_tool(
        self, tool_name: str, params_json: Optional[str] = None
    ) -> int:
        """Execute a tool."""
        return self.tool_commands.run_execute_tool(tool_name, params_json)

    def run_list_resources(self) -> int:
        """List available resources."""
        return self.resource_commands.run_list_resources()

    def run_read_resource(self, uri: str) -> int:
        """Read a resource."""
        return self.resource_commands.run_read_resource(uri)

    def run_list_prompts(self) -> int:
        """List available prompts."""
        return self.prompt_commands.run_list_prompts()

    def run_get_prompt(
        self, prompt_name: str, args_json: Optional[str] = None
    ) -> int:
        """Get prompt messages."""
        return self.prompt_commands.run_get_prompt(prompt_name, args_json)
