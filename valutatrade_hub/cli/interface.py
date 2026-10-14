"""Командный интерфейс ValutaTrade Hub."""

import shlex

from valutatrade_hub.core import usecases
from valutatrade_hub.core.utils import format_amount, format_rate


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
        elif name == "show-portfolio":
            if current_user is None:
                print("Сначала выполните login")
                continue
            base = args.get("base", "USD").upper()
            try:
                rows, total = usecases.show_portfolio(current_user, base)
            except ValueError as e:
                print(e)
                continue
            if not rows:
                print("У вас пока нет кошельков. Купите валюту командой buy.")
                continue
            print(f"Портфель пользователя '{current_user.username}' (база: {base}):")
            for code, balance, value in rows:
                print(f"- {code}: {format_amount(code, balance)} → {value:.2f} {base}")
            print("---------------------------------")
            print(f"ИТОГО: {total:,.2f} {base}")
        elif name == "buy" or name == "sell":
            if current_user is None:
                print("Сначала выполните login")
                continue
            code = args.get("currency", "").upper()
            if code == "" or args.get("amount") is None:
                print(f"Использование: {name} --currency <код> --amount <количество>")
                continue
            try:
                amount = float(args["amount"])
            except ValueError:
                print("'amount' должен быть положительным числом")
                continue
            try:
                if name == "buy":
                    rate, old, new, total = usecases.buy(current_user, code, amount)
                else:
                    rate, old, new, total = usecases.sell(current_user, code, amount)
            except ValueError as e:
                print(e)
                continue
            if name == "buy":
                print(f"Покупка выполнена: {format_amount(code, amount)} {code} "
                      f"по курсу {rate} USD/{code}")
            else:
                print(f"Продажа выполнена: {format_amount(code, amount)} {code} "
                      f"по курсу {rate} USD/{code}")
            print("Изменения в портфеле:")
            print(f"- {code}: было {format_amount(code, old)} "
                  f"→ стало {format_amount(code, new)}")
            if name == "buy":
                print(f"Оценочная стоимость покупки: {total:,.2f} USD")
            else:
                print(f"Оценочная выручка: {total:,.2f} USD")
        elif name == "get-rate":
            from_code = args.get("from", "").upper()
            to_code = args.get("to", "").upper()
            if from_code == "" or to_code == "":
                print("Использование: get-rate --from <код> --to <код>")
                continue
            try:
                rate, updated = usecases.get_rate(from_code, to_code)
            except ValueError as e:
                print(e)
                continue
            updated = updated.replace("T", " ")
            print(f"Курс {from_code}→{to_code}: {format_rate(rate)} "
                  f"(обновлено: {updated})")
            print(f"Обратный курс {to_code}→{from_code}: {format_rate(1 / rate)}")
        else:
            print(f"Неизвестная команда: {name}")
