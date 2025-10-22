"""
Logging configuration for the application
"""
import logging
import sys
from pathlib import Path

# Create logs directory if it doesn't exist
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Configure logging
def setup_logging():
    """Setup application logging to both file and console"""

    # Root logger
    root_logger = logging.getLogger()

    # Guard: Skip if already configured (prevents duplicate handlers on reload)
    if root_logger.handlers:
        return root_logger

    root_logger.setLevel(logging.DEBUG)

    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    simple_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )

    # File handler - detailed logs
    file_handler = logging.FileHandler(LOGS_DIR / 'app.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)

    # Console handler - simple logs
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)

    # Add handlers to root logger
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Uvicorn logger
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.handlers = []
    uvicorn_logger.addHandler(file_handler)
    uvicorn_logger.addHandler(console_handler)

    # Uvicorn access logger
    uvicorn_access = logging.getLogger("uvicorn.access")
    access_handler = logging.FileHandler(LOGS_DIR / 'access.log', encoding='utf-8')
    access_handler.setFormatter(detailed_formatter)
    uvicorn_access.addHandler(access_handler)

    logging.info("Logging configured - logs will be saved to: logs/app.log")

    return root_logger
