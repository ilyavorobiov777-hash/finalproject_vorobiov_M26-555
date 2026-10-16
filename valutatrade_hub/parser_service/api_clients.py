from abc import ABC, abstractmethod

import requests

from valutatrade_hub.core.exceptions import ApiRequestError
from valutatrade_hub.parser_service.config import ParserConfig


class BaseApiClient(ABC):
    @abstractmethod
    def fetch_rates(self):
        pass


class CoinGeckoClient(BaseApiClient):
    def fetch_rates(self):
        ids = ",".join(ParserConfig.CRYPTO_ID_MAP.values())
        params = {"ids": ids, "vs_currencies": "usd"}
        try:
            response = requests.get(
                ParserConfig.COINGECKO_URL,
                params=params,
                timeout=ParserConfig.REQUEST_TIMEOUT,
            )
        except requests.exceptions.RequestException as e:
            raise ApiRequestError(e)
        if response.status_code != 200:
            raise ApiRequestError(f"код ответа {response.status_code}")

        data = response.json()
        rates = {}
        for code in ParserConfig.CRYPTO_CURRENCIES:
            coin_id = ParserConfig.CRYPTO_ID_MAP[code]
            if coin_id in data:
                rates[f"{code}_USD"] = data[coin_id]["usd"]
        return rates


class ExchangeRateApiClient(BaseApiClient):
    def fetch_rates(self):
        key = ParserConfig.EXCHANGERATE_API_KEY
        if key is None:
            raise ApiRequestError("не задан ключ EXCHANGERATE_API_KEY")
        base = ParserConfig.BASE_CURRENCY
        url = f"{ParserConfig.EXCHANGERATE_API_URL}/{key}/latest/{base}"
        try:
            response = requests.get(url, timeout=ParserConfig.REQUEST_TIMEOUT)
        except requests.exceptions.RequestException as e:
            raise ApiRequestError(e)
        if response.status_code != 200:
            raise ApiRequestError(f"код ответа {response.status_code}")

        data = response.json()
        rates = {}
        for code in ParserConfig.FIAT_CURRENCIES:
            if code in data["rates"]:
                rates[f"{code}_{base}"] = 1 / data["rates"][code]
        return rates