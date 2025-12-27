"""Resource-related CLI commands."""

import json

from src.ui.commands.base_command import BaseCommand


class ResourceCommands(BaseCommand):
    """Handles resource listing and reading commands."""

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
            return self.handle_error(e, "Failed to list resources")

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
            return self.handle_error(e, "Failed to read resource")
