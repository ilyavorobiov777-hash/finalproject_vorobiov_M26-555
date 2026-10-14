"""Модели данных ValutaTrade Hub."""

import hashlib

from valutatrade_hub.core.exceptions import InsufficientFundsError


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
            raise InsufficientFundsError(self._balance, amount, self.currency_code)
        self.balance = self._balance - amount

    def get_balance_info(self):
        """Информация о балансе."""
        return f"{self.currency_code}: {self._balance:.4f}"


EXCHANGE_RATES = {
    "EUR_USD": 1.0786,
    "BTC_USD": 59337.21,
    "RUB_USD": 0.01016,
    "ETH_USD": 3720.00,
}


class Portfolio:
    """Все кошельки одного пользователя."""

    def __init__(self, user_id, wallets=None, user=None):
        self._user_id = user_id
        if wallets is None:
            wallets = {}
        self._wallets = wallets
        self._user = user

    @property
    def user(self):
        """Пользователь, которому принадлежит портфель."""
        return self._user

    @property
    def wallets(self):
        """Копия словаря кошельков."""
        return self._wallets.copy()

    def add_currency(self, currency_code):
        """Добавление нового кошелька."""
        if currency_code in self._wallets:
            raise ValueError(f"Кошелек '{currency_code}' уже есть в портфеле")
        self._wallets[currency_code] = Wallet(currency_code)

    def get_wallet(self, currency_code):
        """Кошелек по коду валюты."""
        return self._wallets.get(currency_code)

    def get_total_value(self, base_currency="USD", rates=None):
        """Общая стоимость всех кошельков в базовой валюте."""
        if rates is None:
            rates = EXCHANGE_RATES
        if base_currency == "USD":
            base_rate = 1
        elif f"{base_currency}_USD" in rates:
            base_rate = rates[f"{base_currency}_USD"]
        else:
            raise ValueError(f"Неизвестная базовая валюта '{base_currency}'")
        total = 0
        for code, wallet in self._wallets.items():
            if code == "USD":
                rate = 1
            elif f"{code}_USD" in rates:
                rate = rates[f"{code}_USD"]
            else:
                raise ValueError(f"Не удалось получить курс для {code}→USD")
            total += wallet.balance * rate
        return total / base_rate
