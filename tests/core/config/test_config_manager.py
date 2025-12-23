"""
Unit tests for ConfigManager.
"""

import pytest
from src.core.config.config_manager import ConfigManager


@pytest.mark.unit
class TestConfigManager:
    """Test suite for ConfigManager class."""

    def test_singleton_pattern(self):
        """Test that ConfigManager implements singleton pattern."""
        config1 = ConfigManager()
        config2 = ConfigManager()
        assert config1 is config2

    def test_get_existing_key(self):
        """Test getting an existing configuration key."""
        config = ConfigManager()
        app_name = config.get('app.name')
        assert app_name is not None
        assert isinstance(app_name, str)

    def test_get_nested_key(self):
        """Test getting nested configuration using dot notation."""
        config = ConfigManager()
        log_level = config.get('logging.level')
        assert log_level is not None

    def test_get_nonexistent_key_with_default(self):
        """Test getting non-existent key returns default value."""
        config = ConfigManager()
        value = config.get('nonexistent.key', 'default_value')
        assert value == 'default_value'

    def test_get_all(self):
        """Test getting all configuration values."""
        config = ConfigManager()
        all_config = config.get_all()
        assert isinstance(all_config, dict)
        assert 'app' in all_config or 'logging' in all_config
