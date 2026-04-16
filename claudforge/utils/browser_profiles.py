import json
import os
import platform
from pathlib import Path
from typing import Dict, List, Optional


def get_chrome_user_data_dir() -> Optional[Path]:
    """Return the platform-specific path to Chrome's User Data directory."""
    system = platform.system()
    home = Path.home()

    if system == "Darwin":  # macOS
        return home / "Library" / "Application Support" / "Google" / "Chrome"
    elif system == "Windows":
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            return Path(local_app_data) / "Google" / "Chrome" / "User Data"
    elif system == "Linux":
        # Check for standard Google Chrome first, then Chromium
        chrome_path = home / ".config" / "google-chrome"
        if chrome_path.exists():
            return chrome_path
        chromium_path = home / ".config" / "chromium"
        if chromium_path.exists():
            return chromium_path
    
    return None


def get_system_profiles() -> List[Dict[str, str]]:
    """
    Discover all Chrome profiles on the current system.
    Returns: List of dicts with {'name': Display Name, 'path': Absolute Path, 'folder': Folder Name}
    """
    user_data_dir = get_chrome_user_data_dir()
    if not user_data_dir or not user_data_dir.exists():
        return []

    local_state_path = user_data_dir / "Local State"
    if not local_state_path.exists():
        return []

    try:
        with open(local_state_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        info_cache = data.get("profile", {}).get("info_cache", {})
        profiles = []
        
        for folder_name, info in info_cache.items():
            display_name = info.get("name") or folder_name
            profile_path = user_data_dir / folder_name
            
            # Verify the directory actually exists
            if profile_path.exists():
                profiles.append({
                    "name": display_name,
                    "path": str(profile_path),
                    "folder": folder_name
                })
        
        # Sort by name, but keep "Default" or primary profiles at top if possible
        return sorted(profiles, key=lambda x: (x["name"].lower() != "default", x["name"].lower()))
        
    except Exception:
        return []


def is_profile_locked(profile_path: str) -> bool:
    """
    Check if a Chrome profile is likely locked by an active instance.
    This check varies by OS but usually involves a 'SingletonLock' file or lock on 'Web Data'.
    """
    p = Path(profile_path)
    system = platform.system()
    
    if system == "Windows":
        # On Windows, we try to rename a file or check if we can open the 'Web Data' DB
        # For simplicity, we check for 'lockfile' or 'SingletonLock' existence
        lock_file = p / "lockfile"
        return lock_file.exists()
    else:
        # macOS/Linux use 'SingletonLock' (symlink)
        lock_file = p / "SingletonLock"
        return lock_file.exists() or lock_file.is_symlink()
