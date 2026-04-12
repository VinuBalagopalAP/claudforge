import zipfile
import shutil
from pathlib import Path


def zip_folder(folder: Path, dest_dir: Path) -> Path:
    """
    Create <dest_dir>/<folder.name>.zip from folder contents.
    Excludes common junk files and ensures skill file is named SKILL.md.
    """
    zip_path = dest_dir / folder.name
    exclude_patterns = {
        ".git",
        ".svn",
        ".hg",
        "__pycache__",
        ".pytest_cache",
        ".vscode",
        ".idea",
        ".DS_Store",
        "node_modules",
        "venv",
        ".venv",
        "_zips",
    }

    def should_exclude(p: Path) -> bool:
        return any(part in exclude_patterns for part in p.parts)

    with zipfile.ZipFile(str(zip_path.with_suffix(".zip")), "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in folder.rglob("*"):
            if file_path.is_file() and not should_exclude(file_path.relative_to(folder.parent)):
                arcname = file_path.relative_to(folder.parent)

                # Enforce SKILL.md case/naming inside the zip
                if arcname.name.lower() == "skill.md" or arcname.name.lower() == "skill.skill":
                    arcname = arcname.parent / "SKILL.md"

                zipf.write(file_path, arcname=arcname)

    return zip_path.with_suffix(".zip")


def cleanup_zips(zip_dir: Path):
    """Remove the temporary zip directory."""
    if zip_dir.exists():
        shutil.rmtree(zip_dir, ignore_errors=True)
