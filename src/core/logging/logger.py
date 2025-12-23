"""
Logging mechanism for the application.
Provides centralized logging with file and console handlers.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Dict, Optional

from src.core.config.config_manager import ConfigManager


class Logger:
    """
    Application logger with file and console output.

    Provides a centralized logging mechanism configured through
    the application's configuration system.
    """

    _loggers: Dict[str, logging.Logger] = {}

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Get or create a logger instance.

        Args:
            name: Logger name (typically module name)

        Returns:
            Configured logger instance
        """
        if name in cls._loggers:
            return cls._loggers[name]

        logger = logging.getLogger(name)
        cls._configure_logger(logger)
        cls._loggers[name] = logger

        return logger

    @classmethod
    def _configure_logger(cls, logger: logging.Logger) -> None:
        """
        Configure logger with handlers and formatters.

        Args:
            logger: Logger instance to configure
        """
        config = ConfigManager()

        # Set logging level
        level_str = config.get('logging.level', 'INFO')
        level = getattr(logging, level_str.upper(), logging.INFO)
        logger.setLevel(level)

        # Avoid duplicate handlers
        if logger.handlers:
            return

        # Get formatter
        formatter = cls._get_formatter(config)

        # Add console handler if enabled
        if config.get('logging.console.enabled', True):
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        # Add file handler if enabled
        if config.get('logging.file.enabled', True):
            file_handler = cls._get_file_handler(config, formatter)
            if file_handler:
                logger.addHandler(file_handler)

        # Prevent propagation to root logger
        logger.propagate = False

    @staticmethod
    def _get_formatter(config: ConfigManager) -> logging.Formatter:
        """
        Create log formatter from configuration.

        Args:
            config: Configuration manager instance

        Returns:
            Configured formatter
        """
        log_format = config.get(
            'logging.format',
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.Formatter(log_format)

    @staticmethod
    def _get_file_handler(
        config: ConfigManager,
        formatter: logging.Formatter
    ) -> Optional[RotatingFileHandler]:
        """
        Create rotating file handler from configuration.

        Args:
            config: Configuration manager instance
            formatter: Log formatter to use

        Returns:
            Configured file handler or None if path invalid
        """
        log_path = config.get('logging.file.path', 'logs/app.log')
        max_bytes = config.get('logging.file.max_bytes', 10485760)
        backup_count = config.get('logging.file.backup_count', 5)

        # Ensure log directory exists
        log_file = Path(log_path)
        log_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            handler = RotatingFileHandler(
                log_path,
                maxBytes=max_bytes,
                backupCount=backup_count
            )
            handler.setFormatter(formatter)
            return handler
        except (OSError, ValueError) as e:
            print(f"Warning: Could not create file handler: {e}")
            return None
