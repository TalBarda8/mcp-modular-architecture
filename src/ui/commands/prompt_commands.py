"""Prompt-related CLI commands."""

import sys
import json
from typing import Optional

from src.ui.commands.base_command import BaseCommand


class PromptCommands(BaseCommand):
    """Handles prompt listing and message generation commands."""

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
            return self.handle_error(e, "Failed to list prompts")

    def run_get_prompt(
        self, prompt_name: str, args_json: Optional[str] = None
    ) -> int:
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
            return self.handle_error(e, "Failed to get prompt")
