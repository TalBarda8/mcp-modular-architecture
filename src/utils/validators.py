"""
Validation utility functions.
Provides common validation helpers for the application.
"""

import re
from typing import Any, List


class Validators:
    """Collection of validation utility methods."""

    @staticmethod
    def is_non_empty_string(value: Any) -> bool:
        """
        Check if value is a non-empty string.

        Args:
            value: Value to check

        Returns:
            True if value is a non-empty string
        """
        return isinstance(value, str) and len(value.strip()) > 0

    @staticmethod
    def is_valid_id(value: Any) -> bool:
        """
        Check if value is a valid ID (alphanumeric with hyphens/underscores).

        Args:
            value: Value to check

        Returns:
            True if value is a valid ID
        """
        if not isinstance(value, str):
            return False
        pattern = r'^[a-zA-Z0-9_-]+$'
        return bool(re.match(pattern, value))

    @staticmethod
    def is_in_range(value: Any, min_val: float, max_val: float) -> bool:
        """
        Check if numeric value is within range.

        Args:
            value: Value to check
            min_val: Minimum value (inclusive)
            max_val: Maximum value (inclusive)

        Returns:
            True if value is in range
        """
        if not isinstance(value, (int, float)):
            return False
        return min_val <= value <= max_val

    @staticmethod
    def has_required_keys(data: dict, required_keys: List[str]) -> bool:
        """
        Check if dictionary has all required keys.

        Args:
            data: Dictionary to check
            required_keys: List of required key names

        Returns:
            True if all required keys are present
        """
        if not isinstance(data, dict):
            return False
        return all(key in data for key in required_keys)
