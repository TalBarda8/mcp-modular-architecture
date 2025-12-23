"""
Unit tests for PromptRegistry.
"""

import pytest
from src.mcp.prompt_registry import PromptRegistry
from src.mcp.prompts.code_review_prompt import CodeReviewPrompt
from src.mcp.prompts.summarize_prompt import SummarizePrompt
from src.core.errors.exceptions import (
    ResourceAlreadyExistsError,
    ResourceNotFoundError
)


@pytest.mark.unit
class TestPromptRegistry:
    """Test suite for PromptRegistry class."""

    @pytest.fixture
    def registry(self):
        """Create a fresh registry for each test."""
        reg = PromptRegistry()
        reg.clear()
        return reg

    @pytest.fixture
    def code_review_prompt(self):
        """Create a code review prompt instance."""
        return CodeReviewPrompt()

    @pytest.fixture
    def summarize_prompt(self):
        """Create a summarize prompt instance."""
        return SummarizePrompt()

    def test_singleton_pattern(self):
        """Test that PromptRegistry implements singleton pattern."""
        registry1 = PromptRegistry()
        registry2 = PromptRegistry()
        assert registry1 is registry2

    def test_register_prompt(self, registry, summarize_prompt):
        """Test registering a prompt."""
        registry.register(summarize_prompt)
        assert 'summarize' in registry
        assert len(registry) == 1

    def test_register_duplicate_prompt_raises_error(
        self,
        registry,
        summarize_prompt
    ):
        """Test that registering duplicate prompt raises error."""
        registry.register(summarize_prompt)

        with pytest.raises(ResourceAlreadyExistsError) as exc_info:
            registry.register(SummarizePrompt())
        assert 'summarize' in str(exc_info.value)

    def test_get_prompt(self, registry, summarize_prompt):
        """Test getting a registered prompt."""
        registry.register(summarize_prompt)
        prompt = registry.get_prompt('summarize')
        assert prompt is summarize_prompt

    def test_get_nonexistent_prompt_raises_error(self, registry):
        """Test that getting non-existent prompt raises error."""
        with pytest.raises(ResourceNotFoundError) as exc_info:
            registry.get_prompt('nonexistent')
        assert 'nonexistent' in str(exc_info.value)

    def test_list_prompts(self, registry, code_review_prompt, summarize_prompt):
        """Test listing all registered prompts."""
        registry.register(code_review_prompt)
        registry.register(summarize_prompt)

        prompts = registry.list_prompts()
        assert len(prompts) == 2
        assert 'code_review' in prompts
        assert 'summarize' in prompts

    def test_get_prompts_metadata(self, registry, summarize_prompt):
        """Test getting prompts metadata."""
        registry.register(summarize_prompt)

        metadata = registry.get_prompts_metadata()
        assert len(metadata) == 1
        assert metadata[0]['name'] == 'summarize'
        assert 'description' in metadata[0]

    def test_unregister_prompt(self, registry, summarize_prompt):
        """Test unregistering a prompt."""
        registry.register(summarize_prompt)
        assert 'summarize' in registry

        registry.unregister('summarize')
        assert 'summarize' not in registry
        assert len(registry) == 0

    def test_unregister_nonexistent_prompt_raises_error(self, registry):
        """Test that unregistering non-existent prompt raises error."""
        with pytest.raises(ResourceNotFoundError):
            registry.unregister('nonexistent')

    def test_clear_registry(self, registry, code_review_prompt, summarize_prompt):
        """Test clearing all prompts from registry."""
        registry.register(code_review_prompt)
        registry.register(summarize_prompt)
        assert len(registry) == 2

        registry.clear()
        assert len(registry) == 0

    def test_contains_operator(self, registry, summarize_prompt):
        """Test the 'in' operator."""
        assert 'summarize' not in registry

        registry.register(summarize_prompt)
        assert 'summarize' in registry
