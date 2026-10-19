# ValutaTrade Hub

Консольное приложение для отслеживания и симуляции торговли валютами.
Пользователь регистрируется, покупает и продаёт фиатные валюты и криптовалюты,
смотрит свой портфель и курсы. Курсы загружаются из CoinGecko и ExchangeRate-API.

Итоговый проект по курсу «Программирование на Python», Воробьёв Илья, группа М26-555.

## Структура

```
finalproject_vorobiov_M26-555/
├── data/                    # users.json, portfolios.json, rates.json, exchange_rates.json
├── valutatrade_hub/
│   ├── core/                # модели, валюты, исключения, бизнес-логика
│   ├── infra/               # настройки и работа с JSON (синглтоны)
│   ├── parser_service/      # получение курсов из внешних API
│   ├── cli/                 # командный интерфейс
│   ├── decorators.py        # декоратор @log_action
│   └── logging_config.py    # настройка логов
├── main.py
├── Makefile
└── pyproject.toml
```

## Установка

```
make install
```

## Запуск

```
make project
```

Проверка кода линтером:

```
make lint
```

## Команды

```
register --username alice --password 1234
login --username alice --password 1234
buy --currency BTC --amount 0.05
sell --currency BTC --amount 0.01
show-portfolio --base USD
get-rate --from USD --to BTC
update-rates
show-rates --top 2
exit
```

## Особенности

- Выбрана упрощённая модель покупки: при `buy` и `sell` меняется только баланс
  покупаемой или продаваемой валюты, доллары не списываются и не начисляются.
  Стоимость в USD показывается для оценки.
- Повторный `login` заменяет текущего пользователя.