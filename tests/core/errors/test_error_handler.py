"""
Unit tests for ErrorHandler.
"""

import pytest
from src.core.errors.error_handler import ErrorHandler
from src.core.errors.exceptions import ValidationError


@pytest.mark.unit
class TestErrorHandler:
    """Test suite for ErrorHandler class."""

    @pytest.fixture
    def error_handler(self):
        """Create an error handler instance."""
        return ErrorHandler("test_module")

    def test_safe_execute_success(self):
        """Test safe_execute with successful function."""
        def successful_func(a, b):
            return a + b

        result = ErrorHandler.safe_execute(
            successful_func,
            5, 3
        )
        assert result == 8

    def test_safe_execute_with_exception(self):
        """Test safe_execute with failing function returns default."""
        def failing_func():
            raise ValueError("Test error")

        result = ErrorHandler.safe_execute(
            failing_func,
            default="default_value"
        )
        assert result == "default_value"

    def test_safe_execute_with_custom_default(self):
        """Test safe_execute with custom default value."""
        def failing_func(x):
            raise RuntimeError("Error")

        result = ErrorHandler.safe_execute(
            failing_func,
            42,
            default=None
        )
        assert result is None

    def test_handle_error_logs_exception(self, error_handler):
        """Test that handle_error processes exception without raising."""
        try:
            raise ValidationError("Test error", {"field": "value"})
        except ValidationError as e:
            # Should not raise
            error_handler.handle_error(e, context={"test": "context"})
