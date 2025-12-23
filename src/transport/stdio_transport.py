"""
STDIO Transport implementation.

Handles communication via standard input/output streams.
This is the recommended transport for MCP servers.
"""

import sys
import json
from typing import Any, Dict, Optional

from src.transport.base_transport import BaseTransport


class STDIOTransport(BaseTransport):
    """
    STDIO-based transport implementation.

    Communicates using stdin for input and stdout for output.
    Messages are exchanged as newline-delimited JSON.

    This is the standard transport mechanism for MCP servers,
    allowing them to be easily integrated with various clients.
    """

    def __init__(self):
        """Initialize STDIO transport."""
        super().__init__("stdio")
        self._input_stream = sys.stdin
        self._output_stream = sys.stdout
        self._error_stream = sys.stderr

    def start(self) -> None:
        """
        Start the STDIO transport.

        Sets the transport to running state.
        STDIO transport is always ready once started.
        """
        self._is_running = True
        self.logger.info("STDIO transport started")

    def stop(self) -> None:
        """
        Stop the STDIO transport.

        Cleanly shuts down the transport.
        """
        self._is_running = False
        self.logger.info("STDIO transport stopped")

    def send_message(self, message: Dict[str, Any]) -> None:
        """
        Send a message via stdout.

        Args:
            message: Message dictionary to send

        The message is serialized to JSON and written to stdout
        followed by a newline.
        """
        try:
            json_message = json.dumps(message)
            self._output_stream.write(json_message + '\n')
            self._output_stream.flush()
            self.logger.debug(f"Sent message: {json_message[:100]}...")
        except Exception as e:
            error_msg = f"Failed to send message: {str(e)}"
            self.logger.error(error_msg)
            self.error_handler.log_exception(e)

    def receive_message(self) -> Optional[Dict[str, Any]]:
        """
        Receive a message from stdin.

        Returns:
            Deserialized message dictionary, or None if no message available

        Reads a line from stdin, deserializes the JSON,
        and returns the message dictionary.
        """
        try:
            line = self._input_stream.readline()

            if not line:
                return None

            line = line.strip()
            if not line:
                return None

            message = json.loads(line)
            self.logger.debug(f"Received message: {str(message)[:100]}...")
            return message
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON received: {str(e)}"
            self.logger.error(error_msg)
            return {
                "error": "parse_error",
                "message": error_msg
            }
        except Exception as e:
            error_msg = f"Failed to receive message: {str(e)}"
            self.logger.error(error_msg)
            self.error_handler.log_exception(e)
            return None

    def run_server(self) -> None:
        """
        Run the STDIO transport server loop.

        Continuously reads messages from stdin, processes them,
        and writes responses to stdout.

        This method blocks until stop() is called or stdin is closed.
        """
        self.start()
        self.logger.info("STDIO server loop started")

        try:
            while self._is_running:
                message = self.receive_message()

                if message is None:
                    # EOF or empty message
                    break

                # Process message through handler
                response = self._handle_message(message)

                # Send response
                self.send_message(response)
        except KeyboardInterrupt:
            self.logger.info("STDIO server interrupted by user")
        except Exception as e:
            self.logger.error(f"STDIO server error: {str(e)}")
            self.error_handler.log_exception(e)
        finally:
            self.stop()
            self.logger.info("STDIO server loop ended")

    def send_error(self, error_message: str, error_code: str = "internal_error") -> None:
        """
        Send an error message.

        Args:
            error_message: Error description
            error_code: Error code identifier

        Utility method for sending error responses.
        """
        error_response = {
            "error": error_code,
            "message": error_message
        }
        self.send_message(error_response)
