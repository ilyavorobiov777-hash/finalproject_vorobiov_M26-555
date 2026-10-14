"""Командный интерфейс ValutaTrade Hub."""

import shlex

from valutatrade_hub.core import usecases


def parse_args(parts):
    """Собирает аргументы вида --имя значение в словарь."""
    args = {}
    i = 0
    while i < len(parts) - 1:
        if parts[i].startswith("--"):
            args[parts[i][2:]] = parts[i + 1]
            i += 2
        else:
            i += 1
    return args


def run():
    """Запускает основной цикл приложения."""
    print("Добро пожаловать в ValutaTrade Hub! Для выхода введите exit.")
    current_user = None
    while True:
        command = input("> ").strip()
        if command == "":
            continue
        parts = shlex.split(command)
        name = parts[0]
        args = parse_args(parts[1:])

        if name == "exit":
            print("До свидания!")
            break
        elif name == "register":
            username = args.get("username")
            password = args.get("password")
            if username is None or password is None:
                print("Использование: register --username <имя> --password <пароль>")
                continue
            try:
                user_id = usecases.register(username, password)
                print(
                    f"Пользователь '{username}' зарегистрирован (id={user_id}). "
                    f"Войдите: login --username {username} --password ****"
                )
            except ValueError as e:
                print(e)
        elif name == "login":
            username = args.get("username")
            password = args.get("password")
            if username is None or password is None:
                print("Использование: login --username <имя> --password <пароль>")
                continue
            try:
                current_user = usecases.login(username, password)
                print(f"Вы вошли как '{current_user.username}'")
            except ValueError as e:
                print(e)
        else:
            print(f"Неизвестная команда: {name}")