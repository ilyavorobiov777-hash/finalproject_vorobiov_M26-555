"""Валюты: базовый класс, фиатные и криптовалюты."""

from abc import ABC, abstractmethod

from valutatrade_hub.core.exceptions import CurrencyNotFoundError


class Currency(ABC):
    """Базовый класс валюты."""

    def __init__(self, name, code):
        if name == "":
            raise ValueError("Название валюты не может быть пустым")
        if code != code.upper() or len(code) < 2 or len(code) > 5 or " " in code:
            raise ValueError(f"Некорректный код валюты '{code}'")
        self.name = name
        self.code = code

    @abstractmethod
    def get_display_info(self):
        """Строка с информацией о валюте."""


class FiatCurrency(Currency):
    """Фиатная валюта."""

    def __init__(self, name, code, issuing_country):
        super().__init__(name, code)
        self.issuing_country = issuing_country

    def get_display_info(self):
        """Строка с информацией о валюте."""
        return f"[FIAT] {self.code} - {self.name} (Issuing: {self.issuing_country})"


class CryptoCurrency(Currency):
    """Криптовалюта."""

    def __init__(self, name, code, algorithm, market_cap):
        super().__init__(name, code)
        self.algorithm = algorithm
        self.market_cap = market_cap

    def get_display_info(self):
        """Строка с информацией о валюте."""
        return (
            f"[CRYPTO] {self.code} - {self.name} "
            f"(Algo: {self.algorithm}, MCAP: {self.market_cap:.2e})"
        )


CURRENCIES = {
    "USD": FiatCurrency("US Dollar", "USD", "United States"),
    "EUR": FiatCurrency("Euro", "EUR", "Eurozone"),
    "GBP": FiatCurrency("British Pound", "GBP", "United Kingdom"),
    "RUB": FiatCurrency("Russian Ruble", "RUB", "Russia"),
    "BTC": CryptoCurrency("Bitcoin", "BTC", "SHA-256", 1.12e12),
    "ETH": CryptoCurrency("Ethereum", "ETH", "Ethash", 4.5e11),
    "SOL": CryptoCurrency("Solana", "SOL", "Proof of History", 6.5e10),
}


def get_currency(code):
    """Возвращает валюту по коду."""
    if code not in CURRENCIES:
        raise CurrencyNotFoundError(code)
    return CURRENCIES[code]