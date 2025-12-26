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
        # Verify all three MCP primitives are supported
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

    def test_register_resource_before_init(self, server):
        """Test registering resource before initialization raises error."""
        from src.mcp.resources.config_resource import ConfigResource
        resource = ConfigResource()
        
        with pytest.raises(ServiceError) as exc_info:
            server.register_resource(resource)
        assert "not initialized" in str(exc_info.value).lower()

    def test_register_prompt_before_init(self, server):
        """Test registering prompt before initialization raises error."""
        from src.mcp.prompts.code_review_prompt import CodeReviewPrompt
        prompt = CodeReviewPrompt()
        
        with pytest.raises(ServiceError) as exc_info:
            server.register_prompt(prompt)
        assert "not initialized" in str(exc_info.value).lower()

    def test_read_resource_before_init(self, server):
        """Test reading resource before initialization returns error."""
        result = server.read_resource("config://app")
        assert 'error' in result
        assert "not initialized" in result['error'].lower()

    def test_get_prompt_messages_before_init(self, server):
        """Test getting prompt messages before initialization returns error."""
        result = server.get_prompt_messages("test_prompt")
        assert result['success'] is False
        assert 'error' in result
        assert "not initialized" in result['error'].lower()

    def test_read_resource_with_exception(self, server):
        """Test reading non-existent resource handles exception."""
        server.initialize()
        result = server.read_resource("nonexistent://resource")
        assert 'error' in result

    def test_get_prompt_messages_with_exception(self, server):
        """Test getting messages for non-existent prompt handles exception."""
        server.initialize()
        result = server.get_prompt_messages("nonexistent_prompt")
        assert result['success'] is False
        assert 'error' in result

    def test_get_resources_metadata(self, server):
        """Test getting metadata for all resources."""
        from src.mcp.resources.config_resource import ConfigResource
        from src.mcp.resources.status_resource import StatusResource
        
        server.initialize(resources=[ConfigResource(), StatusResource()])
        metadata = server.get_resources_metadata()
        
        assert len(metadata) == 2
        assert any(r['uri'] == 'config://app' for r in metadata)
        assert any(r['uri'] == 'status://system' for r in metadata)

    def test_get_prompts_metadata(self, server):
        """Test getting metadata for all prompts."""
        from src.mcp.prompts.code_review_prompt import CodeReviewPrompt
        from src.mcp.prompts.summarize_prompt import SummarizePrompt
        
        server.initialize(prompts=[CodeReviewPrompt(), SummarizePrompt()])
        metadata = server.get_prompts_metadata()
        
        assert len(metadata) == 2
        assert any(p['name'] == 'code_review' for p in metadata)
        assert any(p['name'] == 'summarize' for p in metadata)

    def test_initialize_with_invalid_tool(self, server):
        """Test initialization handles tool registration failure gracefully."""
        # Create a mock tool that will fail to register
        class FailingTool:
            def __init__(self):
                self.name = None  # This will cause registration to fail
                
        # Should not raise, but log error
        server.initialize(tools=[FailingTool()])
        # Server should still be initialized even if tool registration failed
        assert server.is_initialized

    def test_initialize_with_invalid_resource(self, server):
        """Test initialization handles resource registration failure gracefully."""
        class FailingResource:
            def __init__(self):
                self.uri = None  # This will cause registration to fail
                
        # Should not raise, but log error
        server.initialize(resources=[FailingResource()])
        assert server.is_initialized

    def test_initialize_with_invalid_prompt(self, server):
        """Test initialization handles prompt registration failure gracefully."""
        class FailingPrompt:
            def __init__(self):
                self.name = None  # This will cause registration to fail
                
        # Should not raise, but log error
        server.initialize(prompts=[FailingPrompt()])
        assert server.is_initialized
