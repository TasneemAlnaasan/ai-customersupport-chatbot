
import logging
import sys
import os
from datetime import datetime


def setup_logger(log_level: str = "INFO") -> None:
    os.makedirs("logs", exist_ok=True)
    log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    handlers = [
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(
            f"logs/app_{datetime.now().strftime('%Y%m%d')}.log",
            encoding="utf-8"
        )
    ]

    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format=log_format,
        datefmt=date_format,
        handlers=handlers
    )

    for lib in ["httpx", "chromadb", "urllib3", "httpcore"]:
        logging.getLogger(lib).setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)