"""
Base abstraction for MCP Tools.
All tools must inherit from BaseTool and implement the execute method.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict

from src.core.logging.logger import Logger
from src.core.errors.error_handler import ErrorHandler
from src.mcp.schemas.tool_schemas import ToolSchema


class BaseTool(ABC):
    """
    Abstract base class for all MCP tools.

    Provides common functionality for tool registration, validation,
    and execution. All concrete tools must inherit from this class.
    """

    def __init__(self):
        """Initialize the base tool."""
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.error_handler = ErrorHandler(self.__class__.__name__)
        self._schema = self._define_schema()

    @abstractmethod
    def _define_schema(self) -> ToolSchema:
        """
        Define the JSON schema for this tool.

        Must be implemented by concrete tools to specify:
        - Tool name and description
        - Input parameter schema
        - Output schema

        Returns:
            ToolSchema instance defining the tool's interface
        """
        pass

    @abstractmethod
    def _execute_impl(self, params: Dict[str, Any]) -> Any:
        """
        Execute the tool's core logic.

        Must be implemented by concrete tools.

        Args:
            params: Validated input parameters

        Returns:
            Tool execution result
        """
        pass

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the tool with given parameters.

        Handles validation, logging, and error handling.

        Args:
            params: Input parameters for the tool

        Returns:
            Dictionary containing execution result or error
        """
        self.logger.info(f"Executing tool: {self.name}")
        self.logger.debug(f"Parameters: {params}")

        try:
            # Validate input parameters
            if not self._schema.validate_input(params):
                error_msg = f"Invalid parameters for tool {self.name}"
                self.logger.error(error_msg)
                return {
                    'success': False,
                    'error': error_msg
                }

            # Execute tool logic
            result = self._execute_impl(params)

            self.logger.info(f"Tool {self.name} executed successfully")
            return {
                'success': True,
                'result': result
            }

        except Exception as e:
            self.error_handler.handle_error(
                e,
                context={'tool': self.name, 'params': params}
            )
            return {
                'success': False,
                'error': str(e)
            }

    @property
    def name(self) -> str:
        """Get the tool name."""
        return self._schema.name

    @property
    def description(self) -> str:
        """Get the tool description."""
        return self._schema.description

    @property
    def schema(self) -> ToolSchema:
        """Get the tool schema."""
        return self._schema

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert tool to dictionary representation.

        Returns:
            Dictionary containing tool metadata and schema
        """
        return self._schema.to_dict()
