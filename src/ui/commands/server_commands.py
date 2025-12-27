"""Server-related CLI commands."""

from src.ui.commands.base_command import BaseCommand


class ServerCommands(BaseCommand):
    """Handles server information commands."""

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
            return self.handle_error(e, "Failed to get server info")
