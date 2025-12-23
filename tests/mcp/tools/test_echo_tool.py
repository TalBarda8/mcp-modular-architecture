"""
Unit tests for EchoTool.
"""

import pytest
from src.mcp.tools.echo_tool import EchoTool


@pytest.mark.unit
class TestEchoTool:
    """Test suite for EchoTool class."""

    @pytest.fixture
    def tool(self):
        """Create an echo tool instance."""
        return EchoTool()

    def test_tool_metadata(self, tool):
        """Test tool metadata."""
        assert tool.name == 'echo'
        assert 'echo' in tool.description.lower()

    def test_echo_message(self, tool):
        """Test echoing a simple message."""
        result = tool.execute({'message': 'Hello, World!'})
        assert result['success'] is True
        assert result['result']['echo'] == 'Hello, World!'

    def test_echo_empty_string(self, tool):
        """Test echoing an empty string."""
        result = tool.execute({'message': ''})
        assert result['success'] is True
        assert result['result']['echo'] == ''

    def test_echo_special_characters(self, tool):
        """Test echoing message with special characters."""
        message = 'Test @#$% 123 \n\t'
        result = tool.execute({'message': message})
        assert result['success'] is True
        assert result['result']['echo'] == message

    def test_missing_message_parameter(self, tool):
        """Test missing required message parameter."""
        result = tool.execute({})
        assert result['success'] is False
        assert 'invalid' in result['error'].lower()

    def test_schema_to_dict(self, tool):
        """Test schema conversion to dictionary."""
        schema_dict = tool.to_dict()
        assert schema_dict['name'] == 'echo'
        assert 'inputSchema' in schema_dict
        assert 'outputSchema' in schema_dict
