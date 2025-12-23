"""
Unit tests for SummarizePrompt.
"""

import pytest
from src.mcp.prompts.summarize_prompt import SummarizePrompt
from src.core.errors.exceptions import ValidationError


@pytest.mark.unit
class TestSummarizePrompt:
    """Test suite for SummarizePrompt class."""

    @pytest.fixture
    def prompt(self):
        """Create a summarize prompt instance."""
        return SummarizePrompt()

    def test_prompt_metadata(self, prompt):
        """Test prompt metadata."""
        assert prompt.name == 'summarize'
        assert 'summarize' in prompt.description.lower()
        assert len(prompt.arguments) == 2

    def test_get_messages_with_required_args(self, prompt):
        """Test getting messages with required arguments."""
        messages = prompt.get_messages({'text': 'This is a test.'})

        assert isinstance(messages, list)
        assert len(messages) == 2
        assert messages[0]['role'] == 'system'
        assert messages[1]['role'] == 'user'
        assert 'This is a test.' in messages[1]['content']

    def test_get_messages_with_optional_args(self, prompt):
        """Test getting messages with optional arguments."""
        messages = prompt.get_messages({
            'text': 'Sample text',
            'length': 'short'
        })

        assert isinstance(messages, list)
        assert 'short' in messages[0]['content']

    def test_missing_required_argument_raises_error(self, prompt):
        """Test that missing required argument raises error."""
        with pytest.raises(ValidationError) as exc_info:
            prompt.get_messages({})
        assert 'text' in str(exc_info.value)

    def test_get_metadata(self, prompt):
        """Test getting prompt metadata."""
        metadata = prompt.get_metadata()

        assert metadata['name'] == 'summarize'
        assert 'description' in metadata
        assert 'arguments' in metadata
        assert len(metadata['arguments']) == 2

    def test_to_dict(self, prompt):
        """Test prompt to_dict method."""
        prompt_dict = prompt.to_dict()

        assert isinstance(prompt_dict, dict)
        assert prompt_dict['name'] == 'summarize'
