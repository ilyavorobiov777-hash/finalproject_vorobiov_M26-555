"""Вспомогательные функции."""

import json

USERS_FILE = "data/users.json"
PORTFOLIOS_FILE = "data/portfolios.json"
RATES_FILE = "data/rates.json"
CRYPTO_CODES = ["BTC", "ETH", "SOL"]


def load_json(path):
    """Читает данные из JSON-файла."""
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path, data):
    """Сохраняет данные в JSON-файл."""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def format_amount(code, amount):
    """Форматирует сумму: 4 знака для криптовалют, 2 для остальных."""
    if code in CRYPTO_CODES:
        return f"{amount:.4f}"
    return f"{amount:.2f}"
