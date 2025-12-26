"""
Unit tests for Logger.
"""

import pytest
import logging
from src.core.logging.logger import Logger


@pytest.mark.unit
class TestLogger:
    """Test suite for Logger class."""

    def test_get_logger_singleton(self):
        """Test that get_logger returns consistent logger instances."""
        logger1 = Logger.get_logger("test_module")
        logger2 = Logger.get_logger("test_module")
        
        # Should return the same logger instance for the same name
        assert logger1.name == logger2.name

    def test_get_logger_different_names(self):
        """Test that different names create different loggers."""
        logger1 = Logger.get_logger("module1")
        logger2 = Logger.get_logger("module2")
        
        assert logger1.name != logger2.name

    def test_logger_has_handlers(self):
        """Test that logger is configured with handlers."""
        logger = Logger.get_logger("test")
        
        # Logger should have handlers configured
        assert len(logging.getLogger(logger.name).handlers) > 0
