"""
Unit tests for custom exceptions.
"""

import pytest
from src.core.errors.exceptions import (
    BaseApplicationError,
    ConfigurationError,
    ValidationError,
    ServiceError,
    ResourceNotFoundError,
    ResourceAlreadyExistsError
)


@pytest.mark.unit
class TestExceptions:
    """Test suite for custom exception classes."""

    def test_base_error_with_message(self):
        """Test BaseApplicationError with message only."""
        error = BaseApplicationError("Test error")
        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.details == {}

    def test_base_error_with_details(self):
        """Test BaseApplicationError with message and details."""
        details = {'key': 'value'}
        error = BaseApplicationError("Test error", details)
        assert error.message == "Test error"
        assert error.details == details
        assert 'key' in str(error)

    def test_configuration_error(self):
        """Test ConfigurationError inherits from BaseApplicationError."""
        error = ConfigurationError("Config error")
        assert isinstance(error, BaseApplicationError)
        assert error.message == "Config error"

    def test_validation_error(self):
        """Test ValidationError inherits from BaseApplicationError."""
        error = ValidationError("Validation failed")
        assert isinstance(error, BaseApplicationError)

    def test_service_error(self):
        """Test ServiceError inherits from BaseApplicationError."""
        error = ServiceError("Service failed")
        assert isinstance(error, BaseApplicationError)

    def test_resource_not_found_error(self):
        """Test ResourceNotFoundError inherits from BaseApplicationError."""
        error = ResourceNotFoundError("Resource not found")
        assert isinstance(error, BaseApplicationError)

    def test_resource_already_exists_error(self):
        """Test ResourceAlreadyExistsError."""
        error = ResourceAlreadyExistsError("Resource exists")
        assert isinstance(error, BaseApplicationError)
