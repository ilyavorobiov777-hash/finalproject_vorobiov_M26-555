"""Командный интерфейс ValutaTrade Hub."""

import shlex

from prettytable import PrettyTable

from valutatrade_hub.core import usecases
from valutatrade_hub.core.currencies import CURRENCIES
from valutatrade_hub.core.exceptions import (
    ApiRequestError,
    CurrencyNotFoundError,
    InsufficientFundsError,
)
from valutatrade_hub.core.utils import format_amount, format_rate
from valutatrade_hub.infra.settings import SettingsLoader
from valutatrade_hub.logging_config import setup_logging


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
    setup_logging()
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
            default_base = SettingsLoader().get("default_base_currency")
            base = args.get("base", default_base).upper()
            try:
                rows, total = usecases.show_portfolio(current_user, base)
            except CurrencyNotFoundError:
                print(f"Неизвестная базовая валюта '{base}'")
                continue
            except ValueError as e:
                print(e)
                continue
            if not rows:
                print("У вас пока нет кошельков. Купите валюту командой buy.")
                continue
            print(f"Портфель пользователя '{current_user.username}' (база: {base}):")
            table = PrettyTable()
            table.field_names = ["Валюта", "Баланс", f"Стоимость ({base})"]
            for code, balance, value in rows:
                table.add_row([code, format_amount(code, balance), f"{value:,.2f}"])
            print(table)
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
            except InsufficientFundsError as e:
                print(e)
                continue
            except CurrencyNotFoundError as e:
                print(e)
                print("Поддерживаемые валюты: " + ", ".join(CURRENCIES))
                continue
            except ValueError as e:
                print(e)
                continue
            if name == "buy":
                print(f"Покупка выполнена: {format_amount(code, amount)} {code} "
                      f"по курсу {format_rate(rate)} USD/{code}")
            else:
                print(f"Продажа выполнена: {format_amount(code, amount)} {code} "
                      f"по курсу {format_rate(rate)} USD/{code}")
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
            except CurrencyNotFoundError as e:
                print(e)
                print("Поддерживаемые валюты: " + ", ".join(CURRENCIES))
                continue
            except ApiRequestError as e:
                print(e)
                print("Повторите попытку позже или проверьте подключение к сети.")
                continue
            except ValueError as e:
                print(e)
                continue
            updated = updated.replace("T", " ").replace("Z", "")
            print(f"Курс {from_code}→{to_code}: {format_rate(rate)} "
                  f"(обновлено: {updated})")
            print(f"Обратный курс {to_code}→{from_code}: {format_rate(1 / rate)}")
        elif name == "update-rates":
            source = args.get("source")
            if source not in (None, "coingecko", "exchangerate"):
                print("Использование: update-rates [--source coingecko|exchangerate]")
                continue
            log_file = SettingsLoader().get("log_file")
            print("INFO: Starting rates update...")
            try:
                results, count, last_refresh = usecases.update_rates(source)
            except ApiRequestError as e:
                print(f"ERROR: {e}")
                print(f"Update failed. Check {log_file} for details.")
                continue
            has_errors = False
            for client_name, client_count, error in results:
                if error is None:
                    print(f"INFO: Fetching from {client_name}... "
                          f"OK ({client_count} rates)")
                else:
                    print(f"ERROR: Failed to fetch from {client_name}: {error}")
                    has_errors = True
            rates_file = SettingsLoader().get("rates_file")
            print(f"INFO: Writing {count} rates to {rates_file}...")
            if has_errors:
                print(f"Update completed with errors. Check {log_file} for details.")
            else:
                print(f"Update successful. Total rates updated: {count}. "
                      f"Last refresh: {last_refresh}")
        elif name == "show-rates":
            currency = args.get("currency")
            if currency is not None:
                currency = currency.upper()
            base = args.get("base", "USD").upper()
            top = None
            if "top" in args:
                try:
                    top = int(args["top"])
                except ValueError:
                    print("'top' должен быть целым числом")
                    continue
            try:
                rates, updated = usecases.show_rates(currency, top, base)
            except CurrencyNotFoundError:
                print(f"Неизвестная базовая валюта '{base}'")
                continue
            except ValueError as e:
                print(e)
                continue
            print(f"Rates from cache (updated at {updated}):")
            table = PrettyTable()
            table.field_names = ["Пара", "Курс"]
            for pair, rate in rates.items():
                table.add_row([pair, format_rate(rate)])
            print(table)
        else:
            print(f"Неизвестная команда: {name}")
