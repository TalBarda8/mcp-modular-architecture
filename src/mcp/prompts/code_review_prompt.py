"""
Code Review Prompt - Example prompt template.
Provides guidance for code review tasks.
"""

from typing import Any, Dict, List, Optional

from src.mcp.prompts.base_prompt import BasePrompt


class CodeReviewPrompt(BasePrompt):
    """
    Prompt template for code review guidance.

    Demonstrates:
    - Structured prompt with arguments
    - System and user message generation
    - Template-based model guidance

    Note: This is an illustrative example demonstrating architecture.
    """

    def __init__(self):
        """Initialize the code review prompt."""
        super().__init__(
            name="code_review",
            description="Guide model to review code for quality and best practices",
            arguments=[
                {
                    'name': 'code',
                    'description': 'The code to review',
                    'required': True
                },
                {
                    'name': 'language',
                    'description': 'Programming language of the code',
                    'required': False
                },
                {
                    'name': 'focus',
                    'description': 'Specific aspects to focus on (e.g., security, performance)',
                    'required': False
                }
            ]
        )

    def get_messages(self, arguments: Optional[Dict[str, Any]] = None) -> List[Dict[str, str]]:
        """
        Generate code review prompt messages.

        Args:
            arguments: Must contain 'code', optionally 'language' and 'focus'

        Returns:
            List of message dictionaries

        Raises:
            ValidationError: If required arguments are missing
        """
        self.validate_arguments(arguments)
        arguments = arguments or {}

        code = arguments['code']
        language = arguments.get('language', 'unknown')
        focus = arguments.get('focus', 'general best practices')

        self.logger.debug(f"Generating {self.name} prompt for {language}")

        messages = [
            {
                'role': 'system',
                'content': (
                    f"You are an expert code reviewer. "
                    f"Review the following {language} code with focus on: {focus}. "
                    f"Provide constructive feedback on code quality, potential issues, "
                    f"and suggested improvements."
                )
            },
            {
                'role': 'user',
                'content': f"Please review this code:\n\n```{language}\n{code}\n```"
            }
        ]

        return messages
