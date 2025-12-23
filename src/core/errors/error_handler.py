"""
Error handling utilities for the application.
Provides centralized error logging and handling mechanisms.
"""

import sys
import traceback
from typing import Any, Callable, Dict, Optional, TypeVar, cast

from src.core.config.config_manager import ConfigManager
from src.core.logging.logger import Logger
from src.core.errors.exceptions import BaseApplicationError

# Type variable for function return type
T = TypeVar('T')


class ErrorHandler:
    """
    Centralized error handling mechanism.

    Provides utilities for logging and handling exceptions
    according to application configuration.
    """

    def __init__(self, logger_name: str = __name__):
        """
        Initialize the error handler.

        Args:
            logger_name: Name for the logger instance
        """
        self.logger = Logger.get_logger(logger_name)
        self.config = ConfigManager()

    def handle_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        reraise: bool = False
    ) -> None:
        """
        Handle an exception with logging and optional re-raising.

        Args:
            error: Exception to handle
            context: Additional context information
            reraise: Whether to re-raise the exception after handling
        """
        context = context or {}

        # Check if we should log errors
        if self.config.get('error_handling.log_errors', True):
            self._log_error(error, context)

        # Check if we should raise on critical errors
        if reraise or (
            isinstance(error, BaseApplicationError) and
            self.config.get('error_handling.raise_on_critical', False)
        ):
            raise error

    def _log_error(self, error: Exception, context: Dict[str, Any]) -> None:
        """
        Log an error with appropriate level and details.

        Args:
            error: Exception to log
            context: Additional context information
        """
        include_traceback = self.config.get(
            'error_handling.include_traceback',
            True
        )

        error_info = {
            'type': type(error).__name__,
            'message': str(error),
            'context': context
        }

        if isinstance(error, BaseApplicationError):
            error_info['details'] = error.details

        if include_traceback:
            error_info['traceback'] = traceback.format_exc()

        self.logger.error(f"Error occurred: {error_info}")

    @staticmethod
    def safe_execute(
        func: Callable[..., T],
        *args: Any,
        default: Optional[T] = None,
        logger_name: str = __name__,
        **kwargs: Any
    ) -> Optional[T]:
        """
        Execute a function safely, catching and handling exceptions.

        Args:
            func: Function to execute
            *args: Positional arguments for the function
            default: Default value to return on error
            logger_name: Name for the error handler's logger
            **kwargs: Keyword arguments for the function

        Returns:
            Function result or default value on error
        """
        handler = ErrorHandler(logger_name)
        try:
            return func(*args, **kwargs)
        except Exception as e:
            handler.handle_error(e, context={'function': func.__name__})
            return default
