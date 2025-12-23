"""
JSON Schema definitions for MCP Tools.
Provides schema validation and documentation for tool inputs/outputs.
"""

from typing import Any, Dict


class ToolSchema:
    """
    Represents a JSON schema for a tool.

    Provides schema definition for tool parameters and return values,
    enabling validation and documentation.
    """

    def __init__(
        self,
        name: str,
        description: str,
        input_schema: Dict[str, Any],
        output_schema: Dict[str, Any]
    ):
        """
        Initialize a tool schema.

        Args:
            name: Unique tool identifier
            description: Human-readable tool description
            input_schema: JSON schema for input parameters
            output_schema: JSON schema for output/return value
        """
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.output_schema = output_schema

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert schema to dictionary representation.

        Returns:
            Dictionary containing schema information
        """
        return {
            'name': self.name,
            'description': self.description,
            'inputSchema': self.input_schema,
            'outputSchema': self.output_schema
        }

    def validate_input(self, params: Dict[str, Any]) -> bool:
        """
        Validate input parameters against schema.

        Basic validation checking required fields and types.

        Args:
            params: Input parameters to validate

        Returns:
            True if validation passes
        """
        required = self.input_schema.get('required', [])
        properties = self.input_schema.get('properties', {})

        # Check required fields
        for field in required:
            if field not in params:
                return False

        # Check types (basic validation)
        for field, value in params.items():
            if field in properties:
                expected_type = properties[field].get('type')
                if expected_type and not self._check_type(value, expected_type):
                    return False

        return True

    @staticmethod
    def _check_type(value: Any, expected_type: str) -> bool:
        """Check if value matches expected JSON schema type."""
        type_mapping = {
            'string': str,
            'number': (int, float),
            'integer': int,
            'boolean': bool,
            'object': dict,
            'array': list
        }

        expected_python_type = type_mapping.get(expected_type)
        if expected_python_type is None:
            return True

        return isinstance(value, expected_python_type)
