import json
import os
from pathlib import Path
from typing import Any, Dict

CONFIG_DIR = Path.home() / ".claudforge"
CONFIG_FILE = CONFIG_DIR / "config.json"


def _ensure_config_exists():
    """Ensure the config directory and file exist with restricted permissions."""
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        # Enforce 0700 permissions on the global config directory
        try:
            os.chmod(CONFIG_DIR, 0o700)
        except OSError:
            pass
    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, "w") as f:
            json.dump({}, f)


def get_config() -> Dict[str, Any]:
    """Load the global configuration."""
    _ensure_config_exists()
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def get_config_key(key: str, default: Any = None) -> Any:
    """Get a specific key from the config."""
    return get_config().get(key, default)


def set_config_key(key: str, value: Any):
    """Set a specific key in the config."""
    config = get_config()
    config[key] = value
    _ensure_config_exists()
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def clear_config():
    """Clear all configuration."""
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()
