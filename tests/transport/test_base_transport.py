"""
Unit tests for BaseTransport.
"""

import pytest
from src.transport.base_transport import BaseTransport


class MockTransport(BaseTransport):
    """Mock transport for testing."""

    def start(self) -> None:
        self._is_running = True

    def stop(self) -> None:
        self._is_running = False

    def send_message(self, message: dict) -> None:
        pass

    def receive_message(self) -> dict:
        return {}


@pytest.mark.unit
class TestBaseTransport:
    """Test suite for BaseTransport base class."""

    def test_set_message_handler(self):
        """Test setting message handler."""
        transport = MockTransport("test")
        
        def handler(msg):
            return {"response": "ok"}
        
        transport.set_message_handler(handler)
        assert transport._message_handler == handler
