import json
from pathlib import Path
from typing import Set

HISTORY_FILE = ".claudforge_history"

def load_history(batch_dir: Path) -> Set[str]:
    """Load the set of successfully uploaded skill folder names."""
    history_path = batch_dir / HISTORY_FILE
    if not history_path.exists():
        return set()
    
    try:
        with open(history_path, 'r') as f:
            data = json.load(f)
            return set(data.get("uploaded", []))
    except (json.JSONDecodeError, IOError):
        return set()

def save_history(batch_dir: Path, uploaded_folders: Set[str]):
    """Save the updated set of successfully uploaded skill folder names."""
    history_path = batch_dir / HISTORY_FILE
    
    # We load current to merge (handles external changes)
    current = load_history(batch_dir)
    current.update(uploaded_folders)
    
    try:
        with open(history_path, 'w') as f:
            json.dump({"uploaded": sorted(list(current))}, f, indent=2)
    except IOError:
        pass
