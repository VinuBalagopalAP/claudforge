import logging
from pathlib import Path
from rich.logging import RichHandler
from rich.console import Console

# Unified project console
console = Console()

LOG_DIR = Path.home() / ".claudforge" / "logs"
LOG_FILE = LOG_DIR / "claudforge.log"


def setup_logger(name: str = "claudforge", level: int = logging.INFO) -> logging.Logger:
    """
    Setup a centralized logger with Rich terminal output and file persistence.
    """
    if not LOG_DIR.exists():
        LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers if setup_logger is called multiple times
    if logger.handlers:
        return logger
        
    logger.setLevel(level)

    # 1. Rich Terminal Handler
    rich_handler = RichHandler(
        console=console,
        rich_tracebacks=True,
        show_path=False,
        markup=True
    )
    rich_handler.setLevel(level)
    logger.addHandler(rich_handler)

    # 2. File Handler (for persistence/debugging)
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)  # Always capture debug info in files
    logger.addHandler(file_handler)

    return logger

# Singleton-like instance for internal use
logger = setup_logger()
