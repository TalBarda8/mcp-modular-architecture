"""
Unit tests for MCPServer.
"""

import pytest
from src.mcp.server import MCPServer
from src.mcp.tools.calculator_tool import CalculatorTool
from src.mcp.tools.echo_tool import EchoTool
from src.core.errors.exceptions import ServiceError


@pytest.mark.unit
class TestMCPServer:
    """Test suite for MCPServer class."""

    @pytest.fixture
    def server(self):
        """Create a fresh server instance for each test."""
        srv = MCPServer()
        # Clean up the registry from previous tests
        srv.tool_registry.clear()
        return srv

    @pytest.fixture
    def calculator_tool(self):
        """Create a calculator tool instance."""
        return CalculatorTool()

    @pytest.fixture
    def echo_tool(self):
        """Create an echo tool instance."""
        return EchoTool()

    def test_server_initialization(self, server):
        """Test server initialization."""
        assert not server.is_initialized

        server.initialize()
        assert server.is_initialized

    def test_initialize_with_tools(self, server, calculator_tool, echo_tool):
        """Test server initialization with tools."""
        server.initialize(tools=[calculator_tool, echo_tool])

        assert server.is_initialized
        assert len(server.list_tools()) == 2
        assert 'calculator' in server.list_tools()
        assert 'echo' in server.list_tools()

    def test_double_initialization_warning(self, server):
        """Test that double initialization is handled gracefully."""
        server.initialize()
        # Second initialization should not raise error
        server.initialize()
        assert server.is_initialized

    def test_register_tool_before_init_raises_error(self, server, calculator_tool):
        """Test that registering tool before init raises error."""
        with pytest.raises(ServiceError) as exc_info:
            server.register_tool(calculator_tool)
        assert 'not initialized' in str(exc_info.value).lower()

    def test_register_tool_after_init(self, server, calculator_tool):
        """Test registering tool after initialization."""
        server.initialize()
        server.register_tool(calculator_tool)

        assert 'calculator' in server.list_tools()

    def test_list_tools(self, server, calculator_tool, echo_tool):
        """Test listing all tools."""
        server.initialize(tools=[calculator_tool, echo_tool])

        tools = server.list_tools()
        assert len(tools) == 2
        assert 'calculator' in tools
        assert 'echo' in tools

    def test_get_tools_metadata(self, server, calculator_tool):
        """Test getting tools metadata."""
        server.initialize(tools=[calculator_tool])

        metadata = server.get_tools_metadata()
        assert len(metadata) == 1
        assert metadata[0]['name'] == 'calculator'

    def test_execute_tool(self, server, calculator_tool):
        """Test executing a tool."""
        server.initialize(tools=[calculator_tool])

        result = server.execute_tool('calculator', {
            'operation': 'add',
            'a': 5,
            'b': 3
        })

        assert result['success'] is True
        assert result['result']['result'] == 8

    def test_execute_tool_before_init(self, server):
        """Test executing tool before initialization."""
        result = server.execute_tool('calculator', {})
        assert result['success'] is False
        assert 'not initialized' in result['error'].lower()

    def test_execute_nonexistent_tool(self, server):
        """Test executing non-existent tool."""
        server.initialize()

        result = server.execute_tool('nonexistent', {})
        assert result['success'] is False

    def test_get_server_info(self, server, calculator_tool):
        """Test getting server information."""
        server.initialize(tools=[calculator_tool])

        info = server.get_info()
        assert 'name' in info
        assert 'version' in info
        assert info['initialized'] is True
        assert info['tool_count'] == 1
        # Stage 3: All three MCP primitives are now supported
        assert info['capabilities']['tools'] is True
        assert info['capabilities']['resources'] is True
        assert info['capabilities']['prompts'] is True

    def test_shutdown_server(self, server, calculator_tool, echo_tool):
        """Test shutting down the server."""
        server.initialize(tools=[calculator_tool, echo_tool])
        assert server.is_initialized
        assert len(server.tool_registry) == 2

        server.shutdown()
        assert not server.is_initialized
        assert len(server.tool_registry) == 0

    def test_shutdown_before_init(self, server):
        """Test shutdown before initialization."""
        # Should not raise error
        server.shutdown()
        assert not server.is_initialized
