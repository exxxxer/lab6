"""Настройка простого журнала HTTP-запросов."""

import logging
from pathlib import Path


def get_logger():
    logger = logging.getLogger("lab6.requests")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        console = logging.StreamHandler()
        console.setFormatter(fmt)
        logger.addHandler(console)
        log_file = logging.FileHandler(Path(__file__).resolve().parent.parent / "app.log", encoding="utf-8")
        log_file.setFormatter(fmt)
        logger.addHandler(log_file)
    logger.propagate = False
    return logger
