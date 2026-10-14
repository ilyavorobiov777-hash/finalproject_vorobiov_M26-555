"""Вспомогательные функции."""

CRYPTO_CODES = ["BTC", "ETH", "SOL"]


def format_amount(code, amount):
    """Форматирует сумму: 4 знака для криптовалют, 2 для остальных."""
    if code in CRYPTO_CODES:
        return f"{amount:.4f}"
    return f"{amount:.2f}"


def format_rate(rate):
    """Форматирует курс: 8 знаков для маленьких чисел, 2 для остальных."""
    if rate < 1:
        return f"{rate:.8f}"
    return f"{rate:.2f}"