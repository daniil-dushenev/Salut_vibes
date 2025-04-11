import logging
import sys
import os

banner = r"""
███████╗  █████╗  ██╗     ██╗   ██╗ ████████╗ ██╗    
██╔════╝ ██╔══██╗ ██║     ██║   ██║ ╚══██╔══╝ ██║    
███████╗ ███████║ ██║     ██║   ██║    ██║    ██║          
     ██║ ██╔══██║ ██║     ██║   ██║    ██║    ╚═╝          
███████║ ██║  ██║ ███████╗╚██████╔╝    ██║    ██╗          
╚══════╝ ╚═╝  ╚═╝ ╚══════╝ ╚═════╝     ╚═╝    ╚═╝          
                                                 
:::::::::::::::  S  A  L  U  T  ::::::::::::::::::
"""

def setup_logger(name: str = "salut_vibes") -> logging.Logger:
    logger = logging.getLogger(name)

    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    logger.setLevel(log_level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.debug(f"Логгер инициализирован с уровнем: {log_level_str}")
    logger.info(banner)
    return logger

logger = setup_logger()
