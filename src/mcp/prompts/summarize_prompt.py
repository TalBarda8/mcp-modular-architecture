"""
Summarize Prompt - Simple example prompt template.
Provides guidance for text summarization tasks.
"""

from typing import Any, Dict, List, Optional

from src.mcp.prompts.base_prompt import BasePrompt


class SummarizePrompt(BasePrompt):
    """
    Prompt template for text summarization.

    Demonstrates:
    - Simple prompt with minimal arguments
    - Single required parameter
    - Basic message generation

    Note: This is an illustrative example demonstrating architecture.
    """

    def __init__(self):
        """Initialize the summarize prompt."""
        super().__init__(
            name="summarize",
            description="Guide model to summarize text content",
            arguments=[
                {
                    'name': 'text',
                    'description': 'The text to summarize',
                    'required': True
                },
                {
                    'name': 'length',
                    'description': 'Desired summary length (short, medium, long)',
                    'required': False
                }
            ]
        )

    def get_messages(self, arguments: Optional[Dict[str, Any]] = None) -> List[Dict[str, str]]:
        """
        Generate summarization prompt messages.

        Args:
            arguments: Must contain 'text', optionally 'length'

        Returns:
            List of message dictionaries

        Raises:
            ValidationError: If required arguments are missing
        """
        self.validate_arguments(arguments)
        arguments = arguments or {}

        text = arguments['text']
        length = arguments.get('length', 'medium')

        self.logger.debug(f"Generating {self.name} prompt for {length} summary")

        messages = [
            {
                'role': 'system',
                'content': (
                    f"You are a helpful assistant that creates {length} summaries. "
                    f"Provide a clear, concise summary of the given text."
                )
            },
            {
                'role': 'user',
                'content': f"Please summarize the following text:\n\n{text}"
            }
        ]

        return messages
