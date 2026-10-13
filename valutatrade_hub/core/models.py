"""Модели данных ValutaTrade Hub."""

import hashlib


class User:
    """Пользователь системы."""

    def __init__(self, user_id, username, hashed_password, salt, registration_date):
        self._user_id = user_id
        self.username = username
        self._hashed_password = hashed_password
        self._salt = salt
        self._registration_date = registration_date

    @property
    def user_id(self):
        """Уникальный идентификатор пользователя."""
        return self._user_id

    @property
    def username(self):
        """Имя пользователя."""
        return self._username

    @username.setter
    def username(self, value):
        if value == "":
            raise ValueError("Имя не может быть пустым")
        self._username = value

    @property
    def hashed_password(self):
        """Пароль в зашифрованном виде."""
        return self._hashed_password

    @property
    def salt(self):
        """Соль пользователя."""
        return self._salt

    @property
    def registration_date(self):
        """Дата регистрации пользователя."""
        return self._registration_date

    def get_user_info(self):
        """Возвращает информацию о пользователе без пароля."""
        return {
            "user_id": self._user_id,
            "username": self._username,
            "registration_date": self._registration_date.isoformat(),
        }

    def change_password(self, new_password):
        """Изменяет пароль пользователя."""
        if len(new_password) < 4:
            raise ValueError("Пароль должен быть не короче 4 символов")
        text = new_password + self._salt
        self._hashed_password = hashlib.sha256(text.encode()).hexdigest()

    def verify_password(self, password):
        """Проверяет введенный пароль на совпадение."""
        text = password + self._salt
        return hashlib.sha256(text.encode()).hexdigest() == self._hashed_password


class Wallet:
    """Кошелек пользователя для одной валюты."""

    def __init__(self, currency_code, balance=0.0):
        self.currency_code = currency_code
        self.balance = balance

    @property
    def balance(self):
        """Баланс кошелька."""
        return self._balance

    @balance.setter
    def balance(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Баланс должен быть числом")
        if value < 0:
            raise ValueError("Баланс не может быть отрицательным")
        self._balance = value

    def deposit(self, amount):
        """Пополнение баланса."""
        if amount <= 0:
            raise ValueError("'amount' должен быть положительным числом")
        self.balance = self._balance + amount

    def withdraw(self, amount):
        """Снятие средств."""
        if amount <= 0:
            raise ValueError("'amount' должен быть положительным числом")
        if amount > self._balance:
            code = self.currency_code
            msg = f"Недостаточно средств: доступно {self._balance:.4f} {code}, "
            msg += f"требуется {amount:.4f} {code}"
            raise ValueError(msg)
        self.balance = self._balance - amount

    def get_balance_info(self):
        """Информация о балансе."""
        return f"{self.currency_code}: {self._balance:.4f}"
