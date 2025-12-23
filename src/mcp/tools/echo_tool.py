"""
Echo Tool - Simple example MCP Tool.
This is an illustrative placeholder demonstrating basic tool implementation.
"""

from typing import Any, Dict

from src.mcp.tools.base_tool import BaseTool
from src.mcp.schemas.tool_schemas import ToolSchema


class EchoTool(BaseTool):
    """
    Simple echo tool that returns the input message.

    Demonstrates:
    - Minimal tool implementation
    - Single parameter handling
    - Simple execution logic

    Note: This is a placeholder example to demonstrate architecture.
    """

    def _define_schema(self) -> ToolSchema:
        """Define the echo tool schema."""
        return ToolSchema(
            name='echo',
            description='Echo back the provided message',
            input_schema={
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'description': 'Message to echo back'
                    }
                },
                'required': ['message']
            },
            output_schema={
                'type': 'object',
                'properties': {
                    'echo': {
                        'type': 'string',
                        'description': 'Echoed message'
                    }
                }
            }
        )

    def _execute_impl(self, params: Dict[str, Any]) -> Any:
        """
        Echo back the message.

        Args:
            params: Must contain 'message'

        Returns:
            Dictionary with echoed message
        """
        message = params['message']
        self.logger.debug(f"Echoing message: {message}")

        return {'echo': message}
