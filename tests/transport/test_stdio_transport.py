"""
Unit tests for STDIOTransport.
"""

import pytest
import json
from io import StringIO

from src.transport.stdio_transport import STDIOTransport


@pytest.mark.unit
class TestSTDIOTransport:
    """Test suite for STDIOTransport class."""

    @pytest.fixture
    def transport(self):
        """Create a STDIO transport instance."""
        return STDIOTransport()

    def test_transport_initialization(self, transport):
        """Test STDIO transport initialization."""
        assert transport.name == "stdio"
        assert not transport.is_running()

    def test_start_transport(self, transport):
        """Test starting the transport."""
        transport.start()
        assert transport.is_running()

    def test_stop_transport(self, transport):
        """Test stopping the transport."""
        transport.start()
        assert transport.is_running()

        transport.stop()
        assert not transport.is_running()

    def test_send_message(self, transport):
        """Test sending a message."""
        # Mock output stream
        mock_output = StringIO()
        transport._output_stream = mock_output

        message = {"method": "test", "params": {"value": 42}}
        transport.send_message(message)

        # Get written output
        output = mock_output.getvalue()
        assert output.strip() == json.dumps(message)

    def test_send_complex_message(self, transport):
        """Test sending a complex message."""
        # Mock output stream
        mock_output = StringIO()
        transport._output_stream = mock_output

        message = {
            "method": "tool.execute",
            "params": {
                "name": "calculator",
                "parameters": {"a": 10, "b": 5}
            },
            "id": "req-123"
        }
        transport.send_message(message)

        # Verify JSON serialization
        output = mock_output.getvalue().strip()
        parsed = json.loads(output)
        assert parsed == message

    def test_receive_message(self, transport):
        """Test receiving a message."""
        # Mock input stream
        message = {"method": "test", "params": {"value": 42}}
        mock_input = StringIO(json.dumps(message) + '\n')
        transport._input_stream = mock_input

        received = transport.receive_message()
        assert received == message

    def test_receive_empty_line(self, transport):
        """Test receiving an empty line."""
        # Mock input stream with empty line
        mock_input = StringIO('\n')
        transport._input_stream = mock_input

        received = transport.receive_message()
        assert received is None

    def test_receive_invalid_json(self, transport):
        """Test receiving invalid JSON."""
        # Mock input stream with invalid JSON
        mock_input = StringIO('not valid json\n')
        transport._input_stream = mock_input

        received = transport.receive_message()
        assert received is not None
        assert "error" in received
        assert received["error"] == "parse_error"

    def test_message_handler_set(self, transport):
        """Test setting message handler."""
        def mock_handler(message):
            return {"result": "handled"}

        transport.set_message_handler(mock_handler)
        assert transport._message_handler is not None

    def test_handle_message_with_handler(self, transport):
        """Test message handling with registered handler."""
        def mock_handler(message):
            return {"result": message.get("value", 0) * 2}

        transport.set_message_handler(mock_handler)

        message = {"value": 21}
        response = transport._handle_message(message)
        assert response == {"result": 42}

    def test_handle_message_without_handler(self, transport):
        """Test message handling without registered handler."""
        message = {"method": "test"}
        response = transport._handle_message(message)

        assert "error" in response
        assert "No message handler" in response["error"]

    def test_send_error(self, transport):
        """Test sending an error message."""
        # Mock output stream
        mock_output = StringIO()
        transport._output_stream = mock_output

        transport.send_error("Test error", "test_error_code")

        output = mock_output.getvalue().strip()
        parsed = json.loads(output)
        assert parsed["error"] == "test_error_code"
        assert parsed["message"] == "Test error"
