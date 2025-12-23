"""
Unit tests for TransportHandler.
"""

import pytest

from src.transport.transport_handler import TransportHandler
from src.mcp.server import MCPServer
from src.mcp.tools.calculator_tool import CalculatorTool


@pytest.mark.unit
class TestTransportHandler:
    """Test suite for TransportHandler class."""

    @pytest.fixture
    def server(self):
        """Create MCP server instance."""
        srv = MCPServer()
        srv.tool_registry.clear()
        srv.resource_registry.clear()
        srv.prompt_registry.clear()
        return srv

    @pytest.fixture
    def handler(self, server):
        """Create transport handler instance."""
        return TransportHandler(server)

    def test_handler_initialization(self, handler, server):
        """Test transport handler initialization."""
        assert handler.server is server

    def test_handle_server_info(self, handler, server):
        """Test handling server.info request."""
        server.initialize()

        message = {"method": "server.info", "id": "req-1"}
        response = handler.handle_message(message)

        assert response["success"] is True
        assert "result" in response
        assert "name" in response["result"]
        assert response["id"] == "req-1"

    def test_handle_server_initialize(self, handler, server):
        """Test handling server.initialize request."""
        message = {"method": "server.initialize"}
        response = handler.handle_message(message)

        assert response["success"] is True
        assert response["result"]["status"] == "initialized"
        assert server.is_initialized

    def test_handle_tool_list(self, handler, server):
        """Test handling tool.list request."""
        calculator = CalculatorTool()
        server.initialize(tools=[calculator])

        message = {"method": "tool.list"}
        response = handler.handle_message(message)

        assert response["success"] is True
        assert "tools" in response["result"]
        assert "calculator" in response["result"]["tools"]

    def test_handle_tool_execute(self, handler, server):
        """Test handling tool.execute request."""
        calculator = CalculatorTool()
        server.initialize(tools=[calculator])

        message = {
            "method": "tool.execute",
            "params": {
                "name": "calculator",
                "parameters": {
                    "operation": "add",
                    "a": 10,
                    "b": 5
                }
            },
            "id": "req-2"
        }
        response = handler.handle_message(message)

        assert response["success"] is True
        assert response["result"]["success"] is True
        assert response["result"]["result"]["result"] == 15

    def test_handle_tool_execute_missing_name(self, handler, server):
        """Test handling tool.execute without tool name."""
        server.initialize()

        message = {
            "method": "tool.execute",
            "params": {
                "parameters": {"value": 42}
            }
        }
        response = handler.handle_message(message)

        assert response["success"] is False
        assert "error" in response
        assert "required" in response["error"]["message"].lower()

    def test_handle_resource_list(self, handler, server):
        """Test handling resource.list request."""
        from src.mcp.resources.config_resource import ConfigResource

        config_resource = ConfigResource()
        server.initialize(resources=[config_resource])

        message = {"method": "resource.list"}
        response = handler.handle_message(message)

        assert response["success"] is True
        assert "resources" in response["result"]
        assert "config://app" in response["result"]["resources"]

    def test_handle_resource_read(self, handler, server):
        """Test handling resource.read request."""
        from src.mcp.resources.config_resource import ConfigResource

        config_resource = ConfigResource()
        server.initialize(resources=[config_resource])

        message = {
            "method": "resource.read",
            "params": {"uri": "config://app"}
        }
        response = handler.handle_message(message)

        assert response["success"] is True
        assert "uri" in response["result"]
        assert response["result"]["uri"] == "config://app"

    def test_handle_prompt_list(self, handler, server):
        """Test handling prompt.list request."""
        from src.mcp.prompts.summarize_prompt import SummarizePrompt

        summarize = SummarizePrompt()
        server.initialize(prompts=[summarize])

        message = {"method": "prompt.list"}
        response = handler.handle_message(message)

        assert response["success"] is True
        assert "prompts" in response["result"]
        assert "summarize" in response["result"]["prompts"]

    def test_handle_prompt_get_messages(self, handler, server):
        """Test handling prompt.get_messages request."""
        from src.mcp.prompts.summarize_prompt import SummarizePrompt

        summarize = SummarizePrompt()
        server.initialize(prompts=[summarize])

        message = {
            "method": "prompt.get_messages",
            "params": {
                "name": "summarize",
                "arguments": {"text": "Test text"}
            }
        }
        response = handler.handle_message(message)

        assert response["success"] is True
        assert "messages" in response["result"]
        # The result contains success, prompt, and messages
        assert response["result"]["success"] is True
        assert response["result"]["prompt"] == "summarize"
        assert isinstance(response["result"]["messages"], list)

    def test_handle_unknown_method(self, handler):
        """Test handling unknown method."""
        message = {"method": "unknown.method"}
        response = handler.handle_message(message)

        assert response["success"] is False
        assert "error" in response
        assert response["error"]["code"] == "method_not_found"

    def test_response_with_id(self, handler, server):
        """Test that response includes request ID when provided."""
        server.initialize()

        message = {"method": "server.info", "id": "test-123"}
        response = handler.handle_message(message)

        assert "id" in response
        assert response["id"] == "test-123"

    def test_response_without_id(self, handler, server):
        """Test response when no request ID provided."""
        server.initialize()

        message = {"method": "server.info"}
        response = handler.handle_message(message)

        # Response may or may not have id key when not provided
        assert response["success"] is True
