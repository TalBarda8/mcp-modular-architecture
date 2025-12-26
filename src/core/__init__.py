"""
Core Infrastructure Layer - Stage 1.

Provides foundational services for the entire application:
- Configuration management (YAML-based, zero hard-coding)
- Structured logging
- Error handling and custom exceptions
"""

from src.core.config.config_manager import ConfigManager
from src.core.logging.logger import Logger
from src.core.errors.exceptions import (
    BaseApplicationError,
    ConfigurationError,
    ValidationError,
    ServiceError,
    ResourceNotFoundError,
    ResourceAlreadyExistsError,
)
from src.core.errors.error_handler import ErrorHandler

__all__ = [
    "ConfigManager",
    "Logger",
    "ErrorHandler",
    "BaseApplicationError",
    "ConfigurationError",
    "ValidationError",
    "ServiceError",
    "ResourceNotFoundError",
    "ResourceAlreadyExistsError",
]
