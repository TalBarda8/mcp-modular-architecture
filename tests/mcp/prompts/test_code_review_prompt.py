"""
Unit tests for CodeReviewPrompt.
"""

import pytest
from src.mcp.prompts.code_review_prompt import CodeReviewPrompt
from src.core.errors.exceptions import ValidationError


@pytest.mark.unit
class TestCodeReviewPrompt:
    """Test suite for CodeReviewPrompt class."""

    @pytest.fixture
    def prompt(self):
        """Create a code review prompt instance."""
        return CodeReviewPrompt()

    def test_prompt_metadata(self, prompt):
        """Test prompt metadata."""
        assert prompt.name == 'code_review'
        assert 'review code' in prompt.description.lower()
        assert len(prompt.arguments) == 3

    def test_get_messages_with_required_args(self, prompt):
        """Test getting messages with required arguments."""
        messages = prompt.get_messages({'code': 'def foo(): pass'})

        assert isinstance(messages, list)
        assert len(messages) == 2
        assert messages[0]['role'] == 'system'
        assert messages[1]['role'] == 'user'
        assert 'def foo(): pass' in messages[1]['content']

    def test_get_messages_with_all_args(self, prompt):
        """Test getting messages with all arguments."""
        messages = prompt.get_messages({
            'code': 'print("hello")',
            'language': 'python',
            'focus': 'security'
        })

        assert isinstance(messages, list)
        assert 'python' in messages[0]['content']
        assert 'security' in messages[0]['content']
        assert 'print("hello")' in messages[1]['content']

    def test_missing_required_argument_raises_error(self, prompt):
        """Test that missing required argument raises error."""
        with pytest.raises(ValidationError) as exc_info:
            prompt.get_messages({'language': 'python'})
        assert 'code' in str(exc_info.value)

    def test_get_metadata(self, prompt):
        """Test getting prompt metadata."""
        metadata = prompt.get_metadata()

        assert metadata['name'] == 'code_review'
        assert 'description' in metadata
        assert 'arguments' in metadata
        assert len(metadata['arguments']) == 3

    def test_argument_definitions(self, prompt):
        """Test argument definitions."""
        args = prompt.arguments

        # Check that 'code' is required
        code_arg = next(arg for arg in args if arg['name'] == 'code')
        assert code_arg['required'] is True

        # Check that 'language' is optional
        lang_arg = next(arg for arg in args if arg['name'] == 'language')
        assert lang_arg['required'] is False
