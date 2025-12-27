"""
MCP CLI Interface.

Command-line interface for interacting with MCP servers.
Uses the MCP Client SDK for all server communication.

Note: This module is excluded from unit test coverage (see pyproject.toml).
UI/CLI code is best tested through integration tests, E2E tests, or manual testing,
as unit tests for argparse-based interfaces often provide limited value.
Core business logic is fully unit tested in the SDK, MCP server, and transport layers.
"""  # pragma: no cover

import sys
import argparse
from typing import Optional

from src.sdk.mcp_client import MCPClient
from src.transport.stdio_transport import STDIOTransport
from src.core.logging.logger import Logger
from src.ui.cli_commands import CLICommands


class MCPCLI:
    """
    MCP Command Line Interface.

    Provides a user-friendly CLI for interacting with MCP server
    capabilities including tools, resources, and prompts.

    Uses the MCP Client SDK (not transport or MCP directly).
    """

    def __init__(self):
        """Initialize the CLI."""
        self.logger = Logger.get_logger("MCPCLI")
        self.commands = CLICommands(self.create_client, self.logger)

    def create_client(self) -> MCPClient:
        """
        Create and configure MCP client.

        Returns:
            Configured MCP client instance
        """
        transport = STDIOTransport()
        client = MCPClient(transport)
        return client


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="MCP CLI - Interact with MCP servers",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Server info command
    subparsers.add_parser("info", help="Show server information")

    # Tool commands
    subparsers.add_parser("tools", help="List available tools")

    tool_exec = subparsers.add_parser("tool", help="Execute a tool")
    tool_exec.add_argument("name", help="Tool name")
    tool_exec.add_argument("--params", help="Tool parameters as JSON string")

    # Resource commands
    subparsers.add_parser("resources", help="List available resources")

    resource_read = subparsers.add_parser("resource", help="Read a resource")
    resource_read.add_argument("uri", help="Resource URI")

    # Prompt commands
    subparsers.add_parser("prompts", help="List available prompts")

    prompt_get = subparsers.add_parser("prompt", help="Get prompt messages")
    prompt_get.add_argument("name", help="Prompt name")
    prompt_get.add_argument("--args", help="Prompt arguments as JSON string")

    # Parse arguments
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Create CLI instance and run command
    cli = MCPCLI()

    try:
        if args.command == "info":
            return cli.commands.run_info()
        elif args.command == "tools":
            return cli.commands.run_list_tools()
        elif args.command == "tool":
            return cli.commands.run_execute_tool(args.name, args.params)
        elif args.command == "resources":
            return cli.commands.run_list_resources()
        elif args.command == "resource":
            return cli.commands.run_read_resource(args.uri)
        elif args.command == "prompts":
            return cli.commands.run_list_prompts()
        elif args.command == "prompt":
            return cli.commands.run_get_prompt(args.name, args.args)
        else:
            print(f"Unknown command: {args.command}", file=sys.stderr)
            return 1

    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
