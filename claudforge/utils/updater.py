import urllib.request
import json
from claudforge.utils.logger import logger

def get_latest_version() -> str:
    """Fetch the latest version of claudforge from PyPI."""
    url = "https://pypi.org/pypi/claudforge/json"
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            data = json.load(response)
            return data["info"]["version"]
    except Exception:
        return ""

def check_for_updates(current_version: str):
    """Compare current version with PyPI and log a message if an update is available."""
    latest = get_latest_version()
    if not latest:
        return

    if latest != current_version:
        logger.warning(
            f"🚀 [bold cyan]A new version of ClaudForge is available![/bold cyan] "
            f"([dim]{current_version}[/dim] -> [bold green]{latest}[/bold green])"
        )
        logger.info(f"👉 Run [bold yellow]pip install --upgrade claudforge[/bold yellow] to update.")
