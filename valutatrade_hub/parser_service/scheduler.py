import time

from valutatrade_hub.core.exceptions import ApiRequestError
from valutatrade_hub.infra.settings import SettingsLoader
from valutatrade_hub.parser_service.api_clients import (
    CoinGeckoClient,
    ExchangeRateApiClient,
)
from valutatrade_hub.parser_service.storage import RatesStorage
from valutatrade_hub.parser_service.updater import RatesUpdater


def run_scheduler():
    interval = SettingsLoader().get("rates_ttl_seconds")
    clients = {
        "CoinGecko": CoinGeckoClient(),
        "ExchangeRate-API": ExchangeRateApiClient(),
    }
    updater = RatesUpdater(clients, RatesStorage())
    while True:
        try:
            results, count, last_refresh = updater.run_update()
            print(f"Обновлено курсов: {count} ({last_refresh})")
        except ApiRequestError as e:
            print(e)
        time.sleep(interval)