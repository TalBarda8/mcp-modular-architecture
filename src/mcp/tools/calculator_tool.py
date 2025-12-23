"""
Calculator Tool - Example MCP Tool for arithmetic operations.
This is an illustrative placeholder demonstrating tool implementation.
"""

from typing import Any, Dict

from src.mcp.tools.base_tool import BaseTool
from src.mcp.schemas.tool_schemas import ToolSchema
from src.core.errors.exceptions import ValidationError


class CalculatorTool(BaseTool):
    """
    Example tool for basic arithmetic calculations.

    Demonstrates:
    - Tool with multiple input parameters
    - Parameter validation
    - Business logic implementation
    - Error handling

    Note: This is a placeholder example to demonstrate architecture.
    """

    def _define_schema(self) -> ToolSchema:
        """Define the calculator tool schema."""
        return ToolSchema(
            name='calculator',
            description='Perform basic arithmetic operations (add, subtract, multiply, divide)',
            input_schema={
                'type': 'object',
                'properties': {
                    'operation': {
                        'type': 'string',
                        'enum': ['add', 'subtract', 'multiply', 'divide'],
                        'description': 'Arithmetic operation to perform'
                    },
                    'a': {
                        'type': 'number',
                        'description': 'First operand'
                    },
                    'b': {
                        'type': 'number',
                        'description': 'Second operand'
                    }
                },
                'required': ['operation', 'a', 'b']
            },
            output_schema={
                'type': 'object',
                'properties': {
                    'result': {
                        'type': 'number',
                        'description': 'Calculation result'
                    }
                }
            }
        )

    def _execute_impl(self, params: Dict[str, Any]) -> Any:
        """
        Execute the calculation.

        Args:
            params: Must contain 'operation', 'a', and 'b'

        Returns:
            Calculation result

        Raises:
            ValidationError: If operation is invalid or division by zero
        """
        operation = params['operation']
        a = params['a']
        b = params['b']

        self.logger.debug(f"Calculating: {a} {operation} {b}")

        if operation == 'add':
            result = a + b
        elif operation == 'subtract':
            result = a - b
        elif operation == 'multiply':
            result = a * b
        elif operation == 'divide':
            if b == 0:
                raise ValidationError(
                    "Division by zero is not allowed",
                    {'a': a, 'b': b}
                )
            result = a / b
        else:
            raise ValidationError(
                f"Invalid operation: {operation}",
                {'operation': operation}
            )

        return {'result': result}
