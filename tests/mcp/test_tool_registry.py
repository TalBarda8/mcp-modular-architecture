"""
Unit tests for ToolRegistry.
"""

import pytest
from src.mcp.tool_registry import ToolRegistry
from src.mcp.tools.calculator_tool import CalculatorTool
from src.mcp.tools.echo_tool import EchoTool
from src.core.errors.exceptions import (
    ResourceAlreadyExistsError,
    ResourceNotFoundError
)


@pytest.mark.unit
class TestToolRegistry:
    """Test suite for ToolRegistry class."""

    @pytest.fixture
    def registry(self):
        """Create a fresh registry for each test."""
        reg = ToolRegistry()
        reg.clear()
        return reg

    @pytest.fixture
    def calculator_tool(self):
        """Create a calculator tool instance."""
        return CalculatorTool()

    @pytest.fixture
    def echo_tool(self):
        """Create an echo tool instance."""
        return EchoTool()

    def test_singleton_pattern(self):
        """Test that ToolRegistry implements singleton pattern."""
        registry1 = ToolRegistry()
        registry2 = ToolRegistry()
        assert registry1 is registry2

    def test_register_tool(self, registry, calculator_tool):
        """Test registering a tool."""
        registry.register(calculator_tool)
        assert 'calculator' in registry
        assert len(registry) == 1

    def test_register_duplicate_tool_raises_error(
        self,
        registry,
        calculator_tool
    ):
        """Test that registering duplicate tool raises error."""
        registry.register(calculator_tool)

        with pytest.raises(ResourceAlreadyExistsError) as exc_info:
            registry.register(CalculatorTool())
        assert 'calculator' in str(exc_info.value)

    def test_get_tool(self, registry, calculator_tool):
        """Test getting a registered tool."""
        registry.register(calculator_tool)
        tool = registry.get_tool('calculator')
        assert tool is calculator_tool

    def test_get_nonexistent_tool_raises_error(self, registry):
        """Test that getting non-existent tool raises error."""
        with pytest.raises(ResourceNotFoundError) as exc_info:
            registry.get_tool('nonexistent')
        assert 'nonexistent' in str(exc_info.value)

    def test_list_tools(self, registry, calculator_tool, echo_tool):
        """Test listing all registered tools."""
        registry.register(calculator_tool)
        registry.register(echo_tool)

        tools = registry.list_tools()
        assert len(tools) == 2
        assert 'calculator' in tools
        assert 'echo' in tools

    def test_get_tools_metadata(self, registry, calculator_tool):
        """Test getting tools metadata."""
        registry.register(calculator_tool)

        metadata = registry.get_tools_metadata()
        assert len(metadata) == 1
        assert metadata[0]['name'] == 'calculator'
        assert 'description' in metadata[0]

    def test_unregister_tool(self, registry, calculator_tool):
        """Test unregistering a tool."""
        registry.register(calculator_tool)
        assert 'calculator' in registry

        registry.unregister('calculator')
        assert 'calculator' not in registry
        assert len(registry) == 0

    def test_unregister_nonexistent_tool_raises_error(self, registry):
        """Test that unregistering non-existent tool raises error."""
        with pytest.raises(ResourceNotFoundError):
            registry.unregister('nonexistent')

    def test_clear_registry(self, registry, calculator_tool, echo_tool):
        """Test clearing all tools from registry."""
        registry.register(calculator_tool)
        registry.register(echo_tool)
        assert len(registry) == 2

        registry.clear()
        assert len(registry) == 0

    def test_contains_operator(self, registry, calculator_tool):
        """Test the 'in' operator."""
        assert 'calculator' not in registry

        registry.register(calculator_tool)
        assert 'calculator' in registry
