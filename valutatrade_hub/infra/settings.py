"""Настройки проекта."""

import os
import tomllib

DEFAULT_SETTINGS = {
    "users_file": "data/users.json",
    "portfolios_file": "data/portfolios.json",
    "rates_file": "data/rates.json",
    "rates_ttl_seconds": 300,
    "default_base_currency": "USD",
    "log_file": "logs/actions.log",
    "log_format": "%(levelname)s %(asctime)s %(message)s",
}


class SettingsLoader:
    """Загружает настройки из pyproject.toml (секция [tool.valutatrade]).

    Singleton сделан через __new__: это самый простой и читаемый способ.
    При каждом вызове SettingsLoader() возвращается один и тот же объект.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.reload()
        return cls._instance

    def reload(self):
        """Перечитывает настройки."""
        self._settings = DEFAULT_SETTINGS.copy()
        if os.path.exists("pyproject.toml"):
            with open("pyproject.toml", "rb") as file:
                data = tomllib.load(file)
            self._settings.update(data.get("tool", {}).get("valutatrade", {}))

    def get(self, key, default=None):
        """Значение настройки по ключу."""
        return self._settings.get(key, default)