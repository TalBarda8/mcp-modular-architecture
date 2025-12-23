"""
Base Transport abstraction.

Defines the interface for all transport implementations.
Transport layer is responsible for message transmission and reception,
completely decoupled from MCP business logic.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Callable

from src.core.logging.logger import Logger
from src.core.errors.error_handler import ErrorHandler


class BaseTransport(ABC):
    """
    Abstract base class for all transport implementations.

    Transport implementations handle the communication layer,
    including message serialization, transmission, and reception.
    The transport layer is completely independent of MCP logic.
    """

    def __init__(self, name: str):
        """
        Initialize the transport.

        Args:
            name: Name of the transport (e.g., 'stdio', 'http', 'sse')
        """
        self.name = name
        self.logger = Logger.get_logger(f"Transport.{name}")
        self.error_handler = ErrorHandler(f"Transport.{name}")
        self._message_handler: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None
        self._is_running = False

    def set_message_handler(self, handler: Callable[[Dict[str, Any]], Dict[str, Any]]) -> None:
        """
        Set the message handler callback.

        The transport calls this handler when a message is received.
        The handler should process the message and return a response.

        Args:
            handler: Callable that processes messages and returns responses
        """
        self._message_handler = handler
        self.logger.info(f"Message handler set for {self.name} transport")

    @abstractmethod
    def start(self) -> None:
        """
        Start the transport.

        Initialize and start listening for incoming messages.
        This method should be non-blocking or run in a loop.
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        """
        Stop the transport.

        Clean up resources and stop listening for messages.
        """
        pass

    @abstractmethod
    def send_message(self, message: Dict[str, Any]) -> None:
        """
        Send a message through the transport.

        Args:
            message: Message to send (will be serialized by transport)
        """
        pass

    @abstractmethod
    def receive_message(self) -> Optional[Dict[str, Any]]:
        """
        Receive a message from the transport.

        Returns:
            Received message (after deserialization), or None if no message
        """
        pass

    def is_running(self) -> bool:
        """
        Check if transport is currently running.

        Returns:
            True if transport is running, False otherwise
        """
        return self._is_running

    def _handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a received message using the registered handler.

        Args:
            message: Message to process

        Returns:
            Response from the message handler
        """
        if not self._message_handler:
            error_msg = "No message handler set for transport"
            self.logger.error(error_msg)
            return {
                "error": error_msg,
                "message": "Transport not properly initialized"
            }

        try:
            response = self._message_handler(message)
            return response
        except Exception as e:
            error_msg = f"Error handling message: {str(e)}"
            self.logger.error(error_msg)
            return {
                "error": error_msg,
                "message": str(e)
            }
