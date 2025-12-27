"""
MCP CLI Command Implementations.

Contains all command handler methods for the MCP CLI.
"""

import sys
import json
from typing import Optional

from src.sdk.mcp_client import MCPClient


class CLICommands:
    """MCP CLI command implementations."""

    def __init__(self, client_factory, logger):
        """
        Initialize CLI commands.

        Args:
            client_factory: Callable that creates MCPClient instances
            logger: Logger instance
        """
        self.create_client = client_factory
        self.logger = logger

    def run_info(self) -> int:
        """
        Display server information.

        Returns:
            Exit code (0 for success)
        """
        try:
            with self.create_client() as client:
                client.initialize_server()
                info = client.get_server_info()

                print("\n=== MCP Server Information ===")
                print(f"Name: {info.get('name', 'Unknown')}")
                print(f"Version: {info.get('version', 'Unknown')}")
                print(f"Stage: {info.get('stage', 'Unknown')}")
                print(f"Initialized: {info.get('initialized', False)}")

                capabilities = info.get('capabilities', {})
                print("\nCapabilities:")
                print(f"  - Tools: {capabilities.get('tools', False)}")
                print(f"  - Resources: {capabilities.get('resources', False)}")
                print(f"  - Prompts: {capabilities.get('prompts', False)}")

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
