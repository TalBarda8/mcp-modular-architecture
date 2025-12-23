"""
Unit tests for Validators utility class.
"""

import pytest
from src.utils.validators import Validators


@pytest.mark.unit
class TestValidators:
    """Test suite for Validators utility class."""

    def test_is_non_empty_string_valid(self):
        """Test is_non_empty_string with valid string."""
        assert Validators.is_non_empty_string('test')
        assert Validators.is_non_empty_string('hello world')

    def test_is_non_empty_string_invalid(self):
        """Test is_non_empty_string with invalid values."""
        assert not Validators.is_non_empty_string('')
        assert not Validators.is_non_empty_string('   ')
        assert not Validators.is_non_empty_string(123)
        assert not Validators.is_non_empty_string(None)

    def test_is_valid_id_valid(self):
        """Test is_valid_id with valid IDs."""
        assert Validators.is_valid_id('test-1')
        assert Validators.is_valid_id('user_123')
        assert Validators.is_valid_id('ABC123')

    def test_is_valid_id_invalid(self):
        """Test is_valid_id with invalid IDs."""
        assert not Validators.is_valid_id('test id')  # space
        assert not Validators.is_valid_id('test@123')  # special char
        assert not Validators.is_valid_id('')
        assert not Validators.is_valid_id(123)

    def test_is_in_range_valid(self):
        """Test is_in_range with values in range."""
        assert Validators.is_in_range(5, 1, 10)
        assert Validators.is_in_range(1, 1, 10)  # boundary
        assert Validators.is_in_range(10, 1, 10)  # boundary
        assert Validators.is_in_range(5.5, 1.0, 10.0)

    def test_is_in_range_invalid(self):
        """Test is_in_range with values out of range."""
        assert not Validators.is_in_range(0, 1, 10)
        assert not Validators.is_in_range(11, 1, 10)
        assert not Validators.is_in_range('5', 1, 10)  # wrong type

    def test_has_required_keys_valid(self):
        """Test has_required_keys with valid dictionary."""
        data = {'name': 'test', 'age': 25, 'email': 'test@example.com'}
        assert Validators.has_required_keys(data, ['name', 'age'])
        assert Validators.has_required_keys(data, ['name'])

    def test_has_required_keys_invalid(self):
        """Test has_required_keys with missing keys."""
        data = {'name': 'test', 'age': 25}
        assert not Validators.has_required_keys(data, ['name', 'email'])
        assert not Validators.has_required_keys('not a dict', ['key'])
