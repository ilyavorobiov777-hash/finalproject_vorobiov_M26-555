"""Вспомогательные функции."""

import json

USERS_FILE = "data/users.json"
PORTFOLIOS_FILE = "data/portfolios.json"
RATES_FILE = "data/rates.json"


def load_json(path):
    """Читает данные из JSON-файла."""
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path, data):
    """Сохраняет данные в JSON-файл."""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)