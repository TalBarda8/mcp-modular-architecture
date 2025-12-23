"""
Unit tests for CalculatorTool.
"""

import pytest
from src.mcp.tools.calculator_tool import CalculatorTool


@pytest.mark.unit
class TestCalculatorTool:
    """Test suite for CalculatorTool class."""

    @pytest.fixture
    def tool(self):
        """Create a calculator tool instance."""
        return CalculatorTool()

    def test_tool_metadata(self, tool):
        """Test tool metadata."""
        assert tool.name == 'calculator'
        assert 'arithmetic' in tool.description.lower()

    def test_addition(self, tool):
        """Test addition operation."""
        result = tool.execute({
            'operation': 'add',
            'a': 5,
            'b': 3
        })
        assert result['success'] is True
        assert result['result']['result'] == 8

    def test_subtraction(self, tool):
        """Test subtraction operation."""
        result = tool.execute({
            'operation': 'subtract',
            'a': 10,
            'b': 4
        })
        assert result['success'] is True
        assert result['result']['result'] == 6

    def test_multiplication(self, tool):
        """Test multiplication operation."""
        result = tool.execute({
            'operation': 'multiply',
            'a': 6,
            'b': 7
        })
        assert result['success'] is True
        assert result['result']['result'] == 42

    def test_division(self, tool):
        """Test division operation."""
        result = tool.execute({
            'operation': 'divide',
            'a': 20,
            'b': 4
        })
        assert result['success'] is True
        assert result['result']['result'] == 5.0

    def test_division_by_zero(self, tool):
        """Test division by zero raises error."""
        result = tool.execute({
            'operation': 'divide',
            'a': 10,
            'b': 0
        })
        assert result['success'] is False
        assert 'zero' in result['error'].lower()

    def test_invalid_operation(self, tool):
        """Test invalid operation raises error."""
        result = tool.execute({
            'operation': 'invalid',
            'a': 5,
            'b': 3
        })
        assert result['success'] is False

    def test_missing_parameter(self, tool):
        """Test missing required parameter."""
        result = tool.execute({
            'operation': 'add',
            'a': 5
            # Missing 'b'
        })
        assert result['success'] is False
        assert 'invalid' in result['error'].lower()

    def test_schema_to_dict(self, tool):
        """Test schema conversion to dictionary."""
        schema_dict = tool.to_dict()
        assert schema_dict['name'] == 'calculator'
        assert 'inputSchema' in schema_dict
        assert 'outputSchema' in schema_dict
