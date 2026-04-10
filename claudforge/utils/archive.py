import shutil
import time
from pathlib import Path
from typing import List, Tuple

ARCHIVE_DIR = ".claudforge_archive"

def create_snapshot(batch_dir: Path, skill_dir: Path):
    """Create a zipped snapshot of the skill directory in the hidden archive."""
    archive_path = batch_dir / ARCHIVE_DIR / skill_dir.name
    archive_path.mkdir(parents=True, exist_ok=True)
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    zip_name = archive_path / f"{timestamp}"
    
    # shutil.make_archive adds the .zip extension automatically
    shutil.make_archive(str(zip_name), 'zip', skill_dir)
    return f"{timestamp}.zip"

def list_snapshots(batch_dir: Path, skill_name: str) -> List[Tuple[str, str]]:
    """Return a list of (timestamp, filename) for a given skill."""
    archive_path = batch_dir / ARCHIVE_DIR / skill_name
    if not archive_path.exists():
        return []
    
    snapshots = []
    for f in sorted(archive_path.glob("*.zip"), reverse=True):
        # Format timestamp for display: 2024-04-11 12:30:45
        ts_str = f.stem
        try:
            dt = time.strptime(ts_str, "%Y%m%d_%H%M%S")
            display_ts = time.strftime("%Y-%m-%d %H:%M:%S", dt)
            snapshots.append((display_ts, f.name))
        except ValueError:
            snapshots.append((ts_str, f.name))
            
    return snapshots

def get_snapshot_zip(batch_dir: Path, skill_name: str, filename: str) -> Path:
    """Return the path to an archived ZIP."""
    return batch_dir / ARCHIVE_DIR / skill_name / filename
