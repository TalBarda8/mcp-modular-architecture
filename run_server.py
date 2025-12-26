#!/usr/bin/env python3
"""
MCP Server Runner

Standalone script to run the MCP server with STDIO transport.
This allows the CLI and SDK examples to connect to a running server.

Usage:
    python run_server.py
    APP_ENV=server python run_server.py  # Use server-specific config

The server will:
1. Initialize the MCP server with all tools, resources, and prompts
2. Start the STDIO transport server loop
3. Listen for JSON-RPC messages on stdin
4. Send responses to stdout

Note: Uses APP_ENV=server config by default to disable console logging
(console logging would interfere with STDIO JSON-RPC communication).
"""

import sys
import os

# Set server environment if not already set
if 'APP_ENV' not in os.environ:
    os.environ['APP_ENV'] = 'server'

from src.mcp.server import MCPServer
from src.mcp.tools.calculator_tool import CalculatorTool
from src.mcp.tools.echo_tool import EchoTool
from src.mcp.resources.config_resource import ConfigResource
from src.mcp.resources.status_resource import StatusResource
from src.mcp.prompts.code_review_prompt import CodeReviewPrompt
from src.mcp.prompts.summarize_prompt import SummarizePrompt
from src.transport.stdio_transport import STDIOTransport
from src.transport.transport_handler import TransportHandler
from src.core.logging.logger import Logger


def main():
    """Run the MCP server with STDIO transport."""
    logger = Logger.get_logger("ServerRunner")

    try:
        # Initialize MCP server
        logger.info("Initializing MCP server...")
        server = MCPServer()

        server.initialize(
            tools=[CalculatorTool(), EchoTool()],
            resources=[ConfigResource(), StatusResource()],
            prompts=[CodeReviewPrompt(), SummarizePrompt()]
        )

        # Create transport and handler
        logger.info("Starting STDIO transport...")
        transport = STDIOTransport()
        handler = TransportHandler(server)

        # Connect handler to transport
        transport.set_message_handler(handler.handle_message)

        # Run server loop (blocks until interrupted)
        logger.info("MCP server ready. Listening on STDIO...")
        logger.info("Press Ctrl+C to stop the server")
        transport.run_server()

    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
