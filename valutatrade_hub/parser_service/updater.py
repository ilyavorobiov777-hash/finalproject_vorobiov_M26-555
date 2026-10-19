import logging

from valutatrade_hub.core.exceptions import ApiRequestError


class RatesUpdater:
    def __init__(self, clients, storage):
        self.clients = clients
        self.storage = storage

    def run_update(self):
        logger = logging.getLogger("valutatrade")
        logger.info("Starting rates update")
        rates = {}
        sources = {}
        results = []
        for name, client in self.clients.items():
            try:
                client_rates = client.fetch_rates()
            except ApiRequestError as e:
                logger.error(f"Failed to fetch from {name}: {e}")
                results.append((name, None, str(e)))
                continue
            logger.info(f"Fetched {len(client_rates)} rates from {name}")
            results.append((name, len(client_rates), None))
            for pair, rate in client_rates.items():
                rates[pair] = rate
                sources[pair] = name

        if not rates:
            raise ApiRequestError("не удалось получить курсы ни от одного источника")
        last_refresh = self.storage.save(rates, sources)
        logger.info(f"Saved {len(rates)} rates")
        return results, len(rates), last_refresh