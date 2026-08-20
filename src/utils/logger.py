import logging
import sys
# pyrefly: ignore [missing-import]
from src.configs.settings import settings

def setup_logger(name: str = "ai_workspace") -> logging.Logger:
    """
    Sets up a production-ready logger that outputs to console.
    Follows configuration from settings.
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicating logs if setup is called multiple times
    if logger.hasHandlers():
        return logger

    # Set log level based on configuration
    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logger.setLevel(level)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Define log format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()
