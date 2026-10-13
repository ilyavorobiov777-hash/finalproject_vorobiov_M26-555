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