"""Бизнес-логика ValutaTrade Hub."""

import hashlib
import secrets
from datetime import datetime

from valutatrade_hub.core.models import User
from valutatrade_hub.core.utils import (
    PORTFOLIOS_FILE,
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