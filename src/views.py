import json
import logging

from src.config import LOGS_PATH, PATH_SETTINGS
from src.services import search_word_in_operations
from src.utils import (date_str_in_date, filter_operations, find_beginning_date, get_exchange_rate, get_stocks_price,
                       greetings, read_excel_file, top_5_transactions)

logging.basicConfig(
    filename=LOGS_PATH / "views.log",
    encoding="utf-8",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s: %(message)s",
)

views_logger = logging.getLogger("app.views")


def json_answer_main(date: str) -> str:
    "Функция реализации JSON-ответа на веб-странице Главная"

    views_logger.info('Запуск функции "json_answer_main"')
    # Распознавание входящей даты и начальной даты
    last_date = date_str_in_date(date)
    first_date = find_beginning_date(last_date)

    # Создание приветствия
    greeting_answer = {"greeting": greetings(last_date)}

    # Создание данных по картам и суммы операций
    operations_answer = []
    operations = filter_operations(read_excel_file(), first_date, last_date).to_dict()
    for key, value in operations.items():
        operations_answer.append(
            {"last_digits": key[-4:], "total_spent": 0 - value, "cashback": round(0 - value / 100, 2)}
        )
    card_answer = {"cards": operations_answer}

    # Создание данных топ 5 расходов
    top_transactions_answer = []
    operations = top_5_transactions(read_excel_file(), first_date, last_date)
    for row in range(5):
        top_transactions_answer.append(
            {
                "date": operations.loc[row, "Дата платежа"],
                "amount": operations.loc[row, "Сумма платежа"],
                "category": operations.loc[row, "Категория"],
                "description": operations.loc[row, "Описание"],
            }
        )
    top_5_answer = {"top_transactions": top_transactions_answer}

    # Запрос курсов валют
    currency_exchange_rate = []
    with open(PATH_SETTINGS) as file:
        user_settings = json.load(file)
    for key in user_settings["user_currencies"]:
        currency_exchange_rate.append({"currency": key, "rate": get_exchange_rate(key)})
    currency_exchange_rate_answer = {"currency_rates": currency_exchange_rate}

    # Запрос курсов акций
    stocks_prices = []
    for key in user_settings["user_stocks"]:
        stocks_prices.append({"stock": key, "price": get_stocks_price(key)})
    stocks_prices_answer = {"stock_prices": stocks_prices}

    # Сбор всех данных, подготовка для JSON-формата
    answer = dict()
    answer.update(greeting_answer)
    answer.update(card_answer)
    answer.update(top_5_answer)
    answer.update(currency_exchange_rate_answer)
    answer.update(stocks_prices_answer)

    # Создание JSON-строки
    json_answer = json.dumps(answer, ensure_ascii=False, indent=4)
    return json_answer


def json_simple_search(search_word: str) -> str:
    "Функция реализации JSON-ответа Простой поиск в Сервисах"

    views_logger.info('Запуск функции "json_simple_search"')
    simple_search_answer = []
    operations = search_word_in_operations(search_word).reset_index()
    for row in range(len(operations)):
        simple_search_answer.append(
            {
                "date": operations.loc[row, "Дата платежа"],
                "amount": operations.loc[row, "Сумма платежа"],
                "category": operations.loc[row, "Категория"],
                "description": operations.loc[row, "Описание"],
            }
        )
    search = {"search": simple_search_answer}

    answer = dict()
    answer.update(search)

    json_answer = json.dumps(answer, ensure_ascii=False, indent=4)
    return json_answer
