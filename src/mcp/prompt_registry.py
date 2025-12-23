"""
Prompt Registry for managing MCP prompts.
Provides centralized registration and discovery of available prompts.
"""

from typing import Dict, List, Optional

from src.mcp.prompts.base_prompt import BasePrompt
from src.core.logging.logger import Logger
from src.core.errors.exceptions import (
    ResourceAlreadyExistsError,
    ResourceNotFoundError
)


class PromptRegistry:
    """
    Registry for managing available MCP prompts.

    Provides:
    - Prompt registration and unregistration
    - Prompt discovery by name
    - Listing all available prompts
    - Prompt metadata access

    Implements singleton pattern to ensure single source of truth.
    """

    _instance: Optional['PromptRegistry'] = None
    _prompts: Dict[str, BasePrompt] = {}

    def __new__(cls) -> 'PromptRegistry':
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the prompt registry."""
        self.logger = Logger.get_logger(__name__)

    def register(self, prompt: BasePrompt) -> None:
        """
        Register a prompt in the registry.

        Args:
            prompt: Prompt instance to register

        Raises:
            ResourceAlreadyExistsError: If prompt with same name exists
        """
        prompt_name = prompt.name

        if prompt_name in self._prompts:
            raise ResourceAlreadyExistsError(
                f"Prompt '{prompt_name}' is already registered",
                {'prompt_name': prompt_name}
            )

        self._prompts[prompt_name] = prompt
        self.logger.info(f"Registered prompt: {prompt_name}")

    def unregister(self, prompt_name: str) -> None:
        """
        Unregister a prompt from the registry.

        Args:
            prompt_name: Name of prompt to unregister

        Raises:
            ResourceNotFoundError: If prompt not found
        """
        if prompt_name not in self._prompts:
            raise ResourceNotFoundError(
                f"Prompt '{prompt_name}' not found in registry",
                {'prompt_name': prompt_name}
            )

        del self._prompts[prompt_name]
        self.logger.info(f"Unregistered prompt: {prompt_name}")

    def get_prompt(self, prompt_name: str) -> BasePrompt:
        """
        Get a prompt by name.

        Args:
            prompt_name: Name of the prompt

        Returns:
            Prompt instance

        Raises:
            ResourceNotFoundError: If prompt not found
        """
        if prompt_name not in self._prompts:
            raise ResourceNotFoundError(
                f"Prompt '{prompt_name}' not found in registry",
                {'prompt_name': prompt_name}
            )

        return self._prompts[prompt_name]

    def list_prompts(self) -> List[str]:
        """
        List all registered prompt names.

        Returns:
            List of prompt names
        """
        return list(self._prompts.keys())

    def get_prompts_metadata(self) -> List[Dict]:
        """
        Get metadata for all registered prompts.

        Returns:
            List of prompt metadata dictionaries
        """
        return [prompt.to_dict() for prompt in self._prompts.values()]

    def clear(self) -> None:
        """
        Clear all registered prompts.

        Useful for testing and cleanup.
        """
        self._prompts.clear()
        self.logger.info("Cleared all prompts from registry")

    def __len__(self) -> int:
        """Return the number of registered prompts."""
        return len(self._prompts)

    def __contains__(self, prompt_name: str) -> bool:
        """Check if a prompt is registered."""
        return prompt_name in self._prompts
