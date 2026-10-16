import json
import os
from datetime import datetime

from valutatrade_hub.parser_service.config import ParserConfig


class RatesStorage:
    def read_json(self, path, default):
        if not os.path.exists(path):
            return default
        with open(path, encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return default

    def write_json(self, path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def save(self, rates, sources):
        now = datetime.now().replace(microsecond=0).isoformat()

        data = self.read_json(ParserConfig.RATES_FILE_PATH, {})
        pairs = data.get("pairs", {})
        for pair, rate in rates.items():
            pairs[pair] = {"rate": rate, "updated_at": now, "source": sources[pair]}
        self.write_json(
            ParserConfig.RATES_FILE_PATH, {"pairs": pairs, "last_refresh": now}
        )

        history = self.read_json(ParserConfig.HISTORY_FILE_PATH, [])
        for pair, rate in rates.items():
            from_code, to_code = pair.split("_")
            history.append(
                {
                    "id": f"{pair}_{now}",
                    "from_currency": from_code,
                    "to_currency": to_code,
                    "rate": rate,
                    "timestamp": now,
                    "source": sources[pair],
                }
            )
        self.write_json(ParserConfig.HISTORY_FILE_PATH, history)
        return now