"""
Configuration Manager for the application.
Handles loading and accessing configuration values from YAML files.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional
import yaml


class ConfigManager:
    """
    Manages application configuration from YAML files.

    Supports environment-based configuration files and provides
    a centralized way to access configuration values.
    """

    _instance: Optional['ConfigManager'] = None
    _config: Dict[str, Any] = {}

    def __new__(cls) -> 'ConfigManager':
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize the configuration manager."""
        if not self._config:  # Only load once
            self._load_config()

    def _load_config(self) -> None:
        """Load configuration from YAML files."""
        config_dir = self._get_config_directory()
        environment = os.getenv('APP_ENV', 'development')

        # Load base configuration
        base_config_path = config_dir / 'base.yaml'
        if base_config_path.exists():
            with open(base_config_path, 'r') as f:
                self._config = yaml.safe_load(f) or {}

        # Load environment-specific configuration
        env_config_path = config_dir / f'{environment}.yaml'
        if env_config_path.exists():
            with open(env_config_path, 'r') as f:
                env_config = yaml.safe_load(f) or {}
                self._deep_update(self._config, env_config)

        # Load local overrides (not in git)
        local_config_path = config_dir / 'local.yaml'
        if local_config_path.exists():
            with open(local_config_path, 'r') as f:
                local_config = yaml.safe_load(f) or {}
                self._deep_update(self._config, local_config)

    @staticmethod
    def _get_config_directory() -> Path:
        """Get the configuration directory path."""
        # Get project root (parent of src directory)
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent.parent
        return project_root / 'config'

    @staticmethod
    def _deep_update(base: dict, update: dict) -> None:
        """Recursively update nested dictionaries."""
        for key, value in update.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                ConfigManager._deep_update(base[key], value)
            else:
                base[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key.

        Supports nested keys using dot notation (e.g., 'database.host').

        Args:
            key: Configuration key (supports dot notation)
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def get_all(self) -> Dict[str, Any]:
        """
        Get all configuration values.

        Returns:
            Complete configuration dictionary
        """
        return self._config.copy()

    def reload(self) -> None:
        """Reload configuration from files."""
        self._config = {}
        self._load_config()
