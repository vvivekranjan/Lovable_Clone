"""Configuration management for API settings."""

import os
import json
from pathlib import Path
from typing import Optional, Dict, Any


CONFIG_DIR = Path.home() / ".companio"
CONFIG_FILE = CONFIG_DIR / "config.json"


def ensure_config_dir():
    """Ensure the configuration directory exists."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> Dict[str, Any]:
    """Load configuration from file.
    
    Returns:
        Configuration dictionary with api_provider, api_key, and model_name
    """
    ensure_config_dir()
    
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return get_default_config()
    
    return get_default_config()


def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to file.
    
    Args:
        config: Configuration dictionary to save
    """
    ensure_config_dir()
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def get_default_config() -> Dict[str, Any]:
    """Get default configuration.
    
    Returns:
        Default configuration dictionary
    """
    return {
        "api_provider": "google",
        "api_key": os.getenv("GOOGLE_API_KEY", ""),
        "model_name": "gemini-2.5-flash"
    }


def is_configured() -> bool:
    """Check if API is properly configured.
    
    Returns:
        True if API key and model name are set
    """
    config = load_config()
    return bool(config.get("api_key", "").strip() and config.get("model_name", "").strip())


def get_api_key() -> str:
    """Get the current API key.
    
    Returns:
        The configured API key
    """
    config = load_config()
    return config.get("api_key", "")


def get_model_name() -> str:
    """Get the current model name.
    
    Returns:
        The configured model name
    """
    config = load_config()
    return config.get("model_name", "gemini-2.5-flash")


def get_api_provider() -> str:
    """Get the current API provider.
    
    Returns:
        The configured API provider (google, openai, anthropic, etc.)
    """
    config = load_config()
    return config.get("api_provider", "google")


def update_api_config(api_provider: str, api_key: str, model_name: str) -> None:
    """Update API configuration.
    
    Args:
        api_provider: The API provider (google, openai, anthropic, etc.)
        api_key: The API key
        model_name: The model name
    """
    config = {
        "api_provider": api_provider,
        "api_key": api_key,
        "model_name": model_name
    }
    save_config(config)
