"""Бизнес-логика ValutaTrade Hub."""

import hashlib
import secrets
from datetime import datetime

from valutatrade_hub.core.models import Portfolio, User, Wallet
from valutatrade_hub.core.utils import (
    PORTFOLIOS_FILE,
    RATES_FILE,
    USERS_FILE,
    load_json,
    save_json,
)


def register(username, password):
    """Регистрация нового пользователя."""
    users = load_json(USERS_FILE)
    for item in users:
        if item["username"] == username:
            raise ValueError(f"Имя пользователя '{username}' уже занято")
    if len(password) < 4:
        raise ValueError("Пароль должен быть не короче 4 символов")

    user_id = len(users) + 1
    salt = secrets.token_hex(4)
    hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
    date = datetime.now().replace(microsecond=0)
    user = User(user_id, username, hashed_password, salt, date)

    users.append(
        {
            "user_id": user.user_id,
            "username": user.username,
            "hashed_password": user.hashed_password,
            "salt": user.salt,
            "registration_date": user.registration_date.isoformat(),
        }
    )
    save_json(USERS_FILE, users)

    portfolios = load_json(PORTFOLIOS_FILE)
    portfolios.append({"user_id": user_id, "wallets": {}})
    save_json(PORTFOLIOS_FILE, portfolios)
    return user_id


def login(username, password):
    """Вход пользователя в систему."""
    users = load_json(USERS_FILE)
    for item in users:
        if item["username"] == username:
            user = User(
                item["user_id"],
                item["username"],
                item["hashed_password"],
                item["salt"],
                datetime.fromisoformat(item["registration_date"]),
            )
            if not user.verify_password(password):
                raise ValueError("Неверный пароль")
            return user
    raise ValueError(f"Пользователь '{username}' не найден")


def load_rates():
    """Курсы из rates.json в виде словаря {"BTC_USD": 59337.21}."""
    data = load_json(RATES_FILE)
    rates = {}
    for pair, info in data.get("pairs", {}).items():
        rates[pair] = info["rate"]
    if not rates:
        return None
    return rates


def load_portfolio(user):
    """Загружает портфель пользователя из portfolios.json."""
    portfolios = load_json(PORTFOLIOS_FILE)
    wallets = {}
    for item in portfolios:
        if item["user_id"] == user.user_id:
            for code, info in item["wallets"].items():
                wallets[code] = Wallet(code, info["balance"])
    return Portfolio(user.user_id, wallets, user)


def show_portfolio(user, base="USD"):
    """Кошельки пользователя и их стоимость в базовой валюте."""
    portfolio = load_portfolio(user)
    rates = load_rates()
    total = portfolio.get_total_value(base, rates)
    rows = []
    for code, wallet in portfolio.wallets.items():
        one_wallet = Portfolio(user.user_id, {code: wallet})
        value = one_wallet.get_total_value(base, rates)
        rows.append((code, wallet.balance, value))
    return rows, total
