"""
Configuration settings for AgentFleet CLI
"""

import os
import json
from pathlib import Path

# Default settings
DEFAULT_API_URL = "http://localhost:5000/api"
DEFAULT_REGION = "us-central1"

# Config file location
CONFIG_DIR = Path.home() / ".agentfleet"
CONFIG_FILE = CONFIG_DIR / "config.json"

def ensure_config_dir():
    """Ensure config directory exists"""
    CONFIG_DIR.mkdir(exist_ok=True)

def load_config():
    """Load configuration from file"""
    if not CONFIG_FILE.exists():
        return {}
    
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_config(config):
    """Save configuration to file"""
    ensure_config_dir()
    
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def get_setting(key, default=None):
    """Get a setting value from environment or config file"""
    # Check environment first
    env_key = f"AGENTFLEET_{key.upper()}"
    env_value = os.environ.get(env_key)
    if env_value is not None:
        return env_value
    
    # Then check config file
    config = load_config()
    return config.get(key, default)

def set_setting(key, value):
    """Set a setting value in config file"""
    config = load_config()
    config[key] = value
    save_config(config)

def get_api_url():
    """Get the API URL"""
    return get_setting("api_url", DEFAULT_API_URL)

def get_api_key():
    """Get the API key"""
    return get_setting("api_key")
