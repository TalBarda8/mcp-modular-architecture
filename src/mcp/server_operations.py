"""
MCP Server Operations.

Handles tool execution, resource reading, and prompt message generation.
"""

from typing import Any, Dict, Optional


class ServerOperations:
    """MCP Server execution operations."""

    def __init__(self, server):
        """
        Initialize server operations.

        Args:
            server: MCPServer instance
        """
        self.server = server
        self.logger = server.logger
        self.error_handler = server.error_handler
        self.tool_registry = server.tool_registry
        self.resource_registry = server.resource_registry
        self.prompt_registry = server.prompt_registry

    def execute_tool(
        self,
        tool_name: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a tool by name with given parameters.

        Args:
            tool_name: Name of the tool to execute
            params: Tool input parameters

        Returns:
            Tool execution result
        """
        if not self.server.is_initialized:
            return {
                'success': False,
                'error': 'Server not initialized'
            }

        self.logger.info(f"Executing tool: {tool_name}")

        try:
            tool = self.tool_registry.get_tool(tool_name)
            result = tool.execute(params)
            return result

        except Exception as e:
            self.error_handler.handle_error(
                e,
                context={'tool_name': tool_name, 'params': params}
            )
            return {
                'success': False,
                'error': str(e)
            }

    def read_resource(self, resource_uri: str) -> Dict[str, Any]:
        """
        Read a resource by URI.

        Args:
            resource_uri: URI of the resource to read

        Returns:
            Resource content and metadata
        """
        if not self.server.is_initialized:
            return {
                'error': 'Server not initialized'
            }

        self.logger.info(f"Reading resource: {resource_uri}")

        try:
            resource = self.resource_registry.get_resource(resource_uri)
            content = resource.read()
            return content

        except Exception as e:
            self.error_handler.handle_error(
                e,
                context={'resource_uri': resource_uri}
            )
            return {
                'uri': resource_uri,
                'error': str(e)
            }

    def get_prompt_messages(
        self,
        prompt_name: str,
        arguments: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Get prompt messages with given arguments.

        Args:
            prompt_name: Name of the prompt
            arguments: Arguments for the prompt

        Returns:
            Dictionary containing messages or error
        """
        if not self.server.is_initialized:
            return {
                'success': False,
                'error': 'Server not initialized'
            }

        self.logger.info(f"Getting messages for prompt: {prompt_name}")

        try:
            prompt = self.prompt_registry.get_prompt(prompt_name)
            messages = prompt.get_messages(arguments)
            return {
                'success': True,
                'prompt': prompt_name,
                'messages': messages
            }

        except Exception as e:
            self.error_handler.handle_error(
                e,
                context={'prompt_name': prompt_name, 'arguments': arguments}
            )
            return {
                'success': False,
                'error': str(e)
            }
