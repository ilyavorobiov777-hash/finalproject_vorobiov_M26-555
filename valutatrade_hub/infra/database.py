"""Работа с JSON-хранилищем."""

import json
import os

from valutatrade_hub.infra.settings import SettingsLoader


class DatabaseManager:
    """Чтение и запись JSON-файлов с данными.

    Singleton сделан через __new__, как и SettingsLoader.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _read(self, path, default):
        if not os.path.exists(path):
            return default
        try:
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return default

    def _write(self, path, data):
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def load_users(self):
        """Список пользователей."""
        return self._read(SettingsLoader().get("users_file"), [])

    def save_users(self, users):
        """Сохраняет список пользователей."""
        self._write(SettingsLoader().get("users_file"), users)

    def load_portfolios(self):
        """Список портфелей."""
        return self._read(SettingsLoader().get("portfolios_file"), [])

    def save_portfolios(self, portfolios):
        """Сохраняет список портфелей."""
        self._write(SettingsLoader().get("portfolios_file"), portfolios)

    def load_rates(self):
        """Кеш курсов."""
        return self._read(SettingsLoader().get("rates_file"), {})

    def save_rates(self, rates):
        """Сохраняет кеш курсов."""
        self._write(SettingsLoader().get("rates_file"), rates)