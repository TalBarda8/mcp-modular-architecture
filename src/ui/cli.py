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
import json
import argparse
from typing import Optional

from src.sdk.mcp_client import MCPClient
from src.transport.stdio_transport import STDIOTransport
from src.core.logging.logger import Logger


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
        self.client: Optional[MCPClient] = None

    def create_client(self) -> MCPClient:
        """
        Create and configure MCP client.

        Returns:
            Configured MCP client instance
        """
        # Use STDIO transport (can be easily swapped for HTTP, SSE, etc.)
        transport = STDIOTransport()
        client = MCPClient(transport)
        return client

    def run_info(self) -> int:
        """
        Display server information.

        Returns:
            Exit code (0 for success)
        """
        try:
            with self.create_client() as client:
                # Initialize server first
                client.initialize_server()

                # Get server info
                info = client.get_server_info()

                print("\n=== MCP Server Information ===")
                print(f"Name: {info.get('name', 'Unknown')}")
                print(f"Version: {info.get('version', 'Unknown')}")
                print(f"Stage: {info.get('stage', 'Unknown')}")
                print(f"Initialized: {info.get('initialized', False)}")

                # Display capabilities
                capabilities = info.get('capabilities', {})
                print("\nCapabilities:")
                print(f"  - Tools: {capabilities.get('tools', False)}")
                print(f"  - Resources: {capabilities.get('resources', False)}")
                print(f"  - Prompts: {capabilities.get('prompts', False)}")

                # Display counts
                print(f"\nTool Count: {info.get('tool_count', 0)}")
                print(f"Resource Count: {info.get('resource_count', 0)}")
                print(f"Prompt Count: {info.get('prompt_count', 0)}")

                return 0

        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            self.logger.error(f"Failed to get server info: {e}")
            return 1

    def run_list_tools(self) -> int:
        """
        List available tools.

        Returns:
            Exit code (0 for success)
        """
        try:
            with self.create_client() as client:
                client.initialize_server()
                tools = client.list_tools()

                print("\n=== Available Tools ===")
                if tools:
                    for tool in tools:
                        print(f"  - {tool}")
                else:
                    print("  (no tools available)")

                return 0

        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            self.logger.error(f"Failed to list tools: {e}")
            return 1

    def run_execute_tool(self, tool_name: str, params_json: Optional[str] = None) -> int:
        """
        Execute a tool.

        Args:
            tool_name: Name of tool to execute
            params_json: JSON string of tool parameters

        Returns:
            Exit code (0 for success)
        """
        try:
            # Parse parameters
            params = {}
            if params_json:
                params = json.loads(params_json)

            with self.create_client() as client:
                client.initialize_server()
                result = client.execute_tool(tool_name, params)

                print(f"\n=== Tool Execution: {tool_name} ===")
                print(json.dumps(result, indent=2))

                return 0

        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON parameters: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            self.logger.error(f"Failed to execute tool: {e}")
            return 1

    def run_list_resources(self) -> int:
        """
        List available resources.

        Returns:
            Exit code (0 for success)
        """
        try:
            with self.create_client() as client:
                client.initialize_server()
                resources = client.list_resources()

                print("\n=== Available Resources ===")
                if resources:
                    for resource in resources:
                        print(f"  - {resource}")
                else:
                    print("  (no resources available)")

                return 0

        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            self.logger.error(f"Failed to list resources: {e}")
            return 1

    def run_read_resource(self, uri: str) -> int:
        """
        Read a resource.

        Args:
            uri: Resource URI

        Returns:
            Exit code (0 for success)
        """
        try:
            with self.create_client() as client:
                client.initialize_server()
                result = client.read_resource(uri)

                print(f"\n=== Resource: {uri} ===")
                print(json.dumps(result, indent=2))

                return 0

        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            self.logger.error(f"Failed to read resource: {e}")
            return 1

    def run_list_prompts(self) -> int:
        """
        List available prompts.

        Returns:
            Exit code (0 for success)
        """
        try:
            with self.create_client() as client:
                client.initialize_server()
                prompts = client.list_prompts()

                print("\n=== Available Prompts ===")
                if prompts:
                    for prompt in prompts:
                        print(f"  - {prompt}")
                else:
                    print("  (no prompts available)")

                return 0

        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            self.logger.error(f"Failed to list prompts: {e}")
            return 1

    def run_get_prompt(self, prompt_name: str, args_json: Optional[str] = None) -> int:
        """
        Get prompt messages.

        Args:
            prompt_name: Name of prompt
            args_json: JSON string of prompt arguments

        Returns:
            Exit code (0 for success)
        """
        try:
            # Parse arguments
            args = {}
            if args_json:
                args = json.loads(args_json)

            with self.create_client() as client:
                client.initialize_server()
                messages = client.get_prompt_messages(prompt_name, args)

                print(f"\n=== Prompt: {prompt_name} ===")
                for i, msg in enumerate(messages, 1):
                    print(f"\nMessage {i} ({msg.get('role', 'unknown')}):")
                    print(msg.get('content', ''))

                return 0

        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON arguments: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            self.logger.error(f"Failed to get prompt: {e}")
            return 1


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
            return cli.run_info()
        elif args.command == "tools":
            return cli.run_list_tools()
        elif args.command == "tool":
            return cli.run_execute_tool(args.name, args.params)
        elif args.command == "resources":
            return cli.run_list_resources()
        elif args.command == "resource":
            return cli.run_read_resource(args.uri)
        elif args.command == "prompts":
            return cli.run_list_prompts()
        elif args.command == "prompt":
            return cli.run_get_prompt(args.name, args.args)
        else:
            print(f"Unknown command: {args.command}", file=sys.stderr)
            return 1

    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
