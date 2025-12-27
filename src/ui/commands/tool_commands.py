"""Tool-related CLI commands."""

import sys
import json
from typing import Optional

from src.ui.commands.base_command import BaseCommand


class ToolCommands(BaseCommand):
    """Handles tool management and execution commands."""

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
            return self.handle_error(e, "Failed to list tools")

    def run_execute_tool(
        self, tool_name: str, params_json: Optional[str] = None
    ) -> int:
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
            return self.handle_error(e, "Failed to execute tool")
