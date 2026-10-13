"""Командный интерфейс ValutaTrade Hub."""


def run():
    """Запускает основной цикл приложения."""
    print("Добро пожаловать в ValutaTrade Hub! Для выхода введите exit.")
    while True:
        command = input("> ").strip()
        if command == "":
            continue
        if command == "exit":
            print("До свидания!")
            break
        print(f"Неизвестная команда: {command}")