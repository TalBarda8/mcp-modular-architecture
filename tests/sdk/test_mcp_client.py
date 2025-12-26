"""
Unit tests for MCP Client SDK.
"""

import pytest
from unittest.mock import Mock, MagicMock

from src.sdk.mcp_client import MCPClient


@pytest.mark.unit
class TestMCPClient:
    """Test suite for MCP Client SDK."""

    @pytest.fixture
    def mock_transport(self):
        """Create a mock transport."""
        transport = Mock()
        transport.start = Mock()
        transport.stop = Mock()
        transport.send_message = Mock()
        transport.receive_message = Mock()
        return transport

    @pytest.fixture
    def client(self, mock_transport):
        """Create MCP client with mock transport."""
        return MCPClient(mock_transport)

    def test_client_initialization(self, client, mock_transport):
        """Test client initialization."""
        assert client.transport is mock_transport
        assert client._request_id == 0

    def test_connect(self, client, mock_transport):
        """Test connecting to server."""
        client.connect()
        mock_transport.start.assert_called_once()

    def test_disconnect(self, client, mock_transport):
        """Test disconnecting from server."""
        client.disconnect()
        mock_transport.stop.assert_called_once()

    def test_context_manager(self, mock_transport):
        """Test using client as context manager."""
        with MCPClient(mock_transport) as client:
            assert client.transport is mock_transport
            mock_transport.start.assert_called_once()

        mock_transport.stop.assert_called_once()

    def test_next_request_id(self, client):
        """Test request ID generation."""
        id1 = client._next_request_id()
        id2 = client._next_request_id()
        id3 = client._next_request_id()

        assert id1 == "req-1"
        assert id2 == "req-2"
        assert id3 == "req-3"

    def test_send_request_success(self, client, mock_transport):
        """Test successful request sending."""
        # Mock successful response
        mock_transport.receive_message.return_value = {
            "success": True,
            "result": {"data": "test"}
        }

        result = client._send_request("test.method", {"param": "value"})

        # Verify request was sent
        mock_transport.send_message.assert_called_once()
        call_args = mock_transport.send_message.call_args[0][0]
        assert call_args["method"] == "test.method"
        assert call_args["params"] == {"param": "value"}
        assert "id" in call_args

        # Verify result
        assert result == {"data": "test"}

    def test_send_request_error(self, client, mock_transport):
        """Test request with error response."""
        # Mock error response
        mock_transport.receive_message.return_value = {
            "success": False,
            "error": {
                "code": "test_error",
                "message": "Test error message"
            }
        }

        with pytest.raises(Exception) as exc_info:
            client._send_request("test.method")

        assert "Test error message" in str(exc_info.value)

    def test_send_request_no_response(self, client, mock_transport):
        """Test request with no response."""
        mock_transport.receive_message.return_value = None

        with pytest.raises(Exception) as exc_info:
            client._send_request("test.method")

        assert "No response" in str(exc_info.value)

    def test_get_server_info(self, client, mock_transport):
        """Test getting server info."""
        mock_transport.receive_message.return_value = {
            "success": True,
            "result": {
                "name": "Test Server",
                "version": "1.0.0"
            }
        }

        info = client.get_server_info()

        assert info["name"] == "Test Server"
        assert info["version"] == "1.0.0"

        # Verify correct method was called
        call_args = mock_transport.send_message.call_args[0][0]
        assert call_args["method"] == "server.info"

    def test_initialize_server(self, client, mock_transport):
        """Test initializing server."""
        mock_transport.receive_message.return_value = {
            "success": True,
            "result": {"status": "initialized"}
        }

        result = client.initialize_server()

        assert result["status"] == "initialized"

        # Verify correct method was called
        call_args = mock_transport.send_message.call_args[0][0]
        assert call_args["method"] == "server.initialize"

    def test_list_tools(self, client, mock_transport):
        """Test listing tools."""
        mock_transport.receive_message.return_value = {
            "success": True,
            "result": {"tools": ["tool1", "tool2", "tool3"]}
        }

        tools = client.list_tools()

        assert tools == ["tool1", "tool2", "tool3"]

        # Verify correct method was called
        call_args = mock_transport.send_message.call_args[0][0]
        assert call_args["method"] == "tool.list"

    def test_execute_tool(self, client, mock_transport):
        """Test executing a tool."""
        mock_transport.receive_message.return_value = {
            "success": True,
            "result": {
                "success": True,
                "result": {"output": "test output"}
            }
        }

        result = client.execute_tool("calculator", {"operation": "add", "a": 1, "b": 2})

        assert result["success"] is True
        assert result["result"]["output"] == "test output"

        # Verify correct method and params were called
        call_args = mock_transport.send_message.call_args[0][0]
        assert call_args["method"] == "tool.execute"
        assert call_args["params"]["name"] == "calculator"
        assert call_args["params"]["parameters"] == {"operation": "add", "a": 1, "b": 2}

    def test_list_resources(self, client, mock_transport):
        """Test listing resources."""
        mock_transport.receive_message.return_value = {
            "success": True,
            "result": {"resources": ["config://app", "status://system"]}
        }

        resources = client.list_resources()

        assert resources == ["config://app", "status://system"]

        # Verify correct method was called
        call_args = mock_transport.send_message.call_args[0][0]
        assert call_args["method"] == "resource.list"

    def test_read_resource(self, client, mock_transport):
        """Test reading a resource."""
        mock_transport.receive_message.return_value = {
            "success": True,
            "result": {
                "uri": "config://app",
                "content": {"key": "value"}
            }
        }

        result = client.read_resource("config://app")

        assert result["uri"] == "config://app"
        assert result["content"] == {"key": "value"}

        # Verify correct method and params were called
        call_args = mock_transport.send_message.call_args[0][0]
        assert call_args["method"] == "resource.read"
        assert call_args["params"]["uri"] == "config://app"

    def test_list_prompts(self, client, mock_transport):
        """Test listing prompts."""
        mock_transport.receive_message.return_value = {
            "success": True,
            "result": {"prompts": ["code_review", "summarize"]}
        }

        prompts = client.list_prompts()

        assert prompts == ["code_review", "summarize"]

        # Verify correct method was called
        call_args = mock_transport.send_message.call_args[0][0]
        assert call_args["method"] == "prompt.list"

    def test_get_prompt_messages(self, client, mock_transport):
        """Test getting prompt messages."""
        mock_transport.receive_message.return_value = {
            "success": True,
            "result": {
                "success": True,
                "messages": [
                    {"role": "system", "content": "System message"},
                    {"role": "user", "content": "User message"}
                ]
            }
        }

        messages = client.get_prompt_messages("summarize", {"text": "test"})

        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"

        # Verify correct method and params were called
        call_args = mock_transport.send_message.call_args[0][0]
        assert call_args["method"] == "prompt.get_messages"
        assert call_args["params"]["name"] == "summarize"
        assert call_args["params"]["arguments"] == {"text": "test"}

    def test_execute_tool_no_params(self, client, mock_transport):
        """Test executing a tool without parameters."""
        mock_transport.receive_message.return_value = {
            "success": True,
            "result": {"success": True}
        }

        client.execute_tool("echo")

        # Verify empty parameters dict was sent
        call_args = mock_transport.send_message.call_args[0][0]
        assert call_args["params"]["parameters"] == {}

    def test_get_prompt_messages_no_args(self, client, mock_transport):
        """Test getting prompt messages without arguments."""
        mock_transport.receive_message.return_value = {
            "success": True,
            "result": {"success": True, "messages": []}
        }

        client.get_prompt_messages("test_prompt")

        # Verify empty arguments dict was sent
        call_args = mock_transport.send_message.call_args[0][0]
        assert call_args["params"]["arguments"] == {}
