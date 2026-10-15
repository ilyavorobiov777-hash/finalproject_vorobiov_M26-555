"""Настройка логирования."""

import logging
import os

from valutatrade_hub.infra.settings import SettingsLoader


def setup_logging():
    """Настраивает запись логов в файл."""
    settings = SettingsLoader()
    log_file = settings.get("log_file")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    handler = logging.FileHandler(log_file, encoding="utf-8")
    formatter = logging.Formatter(settings.get("log_format"), "%Y-%m-%dT%H:%M:%S")
    handler.setFormatter(formatter)

    logger = logging.getLogger("valutatrade")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        logger.addHandler(handler)