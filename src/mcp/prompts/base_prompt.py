"""
Base abstraction for MCP Prompts.
Prompts are templates for guiding model interactions.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from src.core.logging.logger import Logger
from src.core.errors.error_handler import ErrorHandler
from src.core.errors.exceptions import ValidationError


class BasePrompt(ABC):
    """
    Abstract base class for all MCP prompts.

    Prompts provide template-based guidance for model interactions.
    All concrete prompts must inherit from this class.
    """

    def __init__(
        self,
        name: str,
        description: str,
        arguments: Optional[List[Dict[str, Any]]] = None
    ):
        """
        Initialize the base prompt.

        Args:
            name: Unique prompt identifier
            description: Human-readable prompt description
            arguments: List of argument definitions (name, description, required)
        """
        self.name = name
        self.description = description
        self.arguments = arguments or []
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.error_handler = ErrorHandler(self.__class__.__name__)

    @abstractmethod
    def get_messages(self, arguments: Optional[Dict[str, Any]] = None) -> List[Dict[str, str]]:
        """
        Generate prompt messages with given arguments.

        Must be implemented by concrete prompts.

        Args:
            arguments: Values for prompt arguments

        Returns:
            List of message dictionaries (role, content)

        Raises:
            ValidationError: If required arguments are missing
        """
        pass

    def validate_arguments(self, arguments: Optional[Dict[str, Any]] = None) -> bool:
        """
        Validate provided arguments against prompt definition.

        Args:
            arguments: Arguments to validate

        Returns:
            True if validation passes

        Raises:
            ValidationError: If validation fails
        """
        arguments = arguments or {}

        # Check required arguments
        for arg_def in self.arguments:
            if arg_def.get('required', False):
                arg_name = arg_def['name']
                if arg_name not in arguments:
                    raise ValidationError(
                        f"Required argument '{arg_name}' is missing",
                        {'prompt': self.name, 'missing_argument': arg_name}
                    )

        return True

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get prompt metadata.

        Returns:
            Dictionary containing prompt metadata
        """
        return {
            'name': self.name,
            'description': self.description,
            'arguments': self.arguments
        }

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert prompt to dictionary representation.

        Returns:
            Dictionary containing full prompt information
        """
        return self.get_metadata()

    def __repr__(self) -> str:
        """Return string representation of the prompt."""
        arg_count = len(self.arguments)
        return f"{self.__class__.__name__}(name={self.name}, args={arg_count})"
