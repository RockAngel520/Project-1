import datetime
import logging
import os

import pandas as pd
import requests
from dotenv import load_dotenv

from src.config import LOGS_PATH, PATH_OPERATIONS

logging.basicConfig(
    filename=LOGS_PATH / "utils.log",
    encoding="utf-8",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s: %(message)s",
)

utils_logger = logging.getLogger("app.utils")

load_dotenv()
api_key = os.getenv("API_KEY_ALPHAVANTAGE")


def date_str_in_date(date_str: str) -> datetime:
    "Функция перевода входящего строкового значения даты в дату"
    utils_logger.info('Запуск функции "date_str_in_date"')
    try:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return date
    except ValueError as e:
        utils_logger.error(f"Введено некорректная дата: {date_str}. Ошибка: {str(e)} в функции date_str_in_date")
        print("Дата указана неверно. Правильный формат даты YYYY-MM-DD HH:MM:SS")


def find_beginning_date(date_end: datetime) -> datetime:
    "Функция нахождения начального дня фильтрации данных"
    utils_logger.info('Запуск функции "find_beginning_date"')
    beginning_date = datetime.datetime(date_end.year, date_end.month, 1, 0, 0, 0)
    return beginning_date


def greetings(date) -> str | None:
    "Функция приветствия в зависимости от входящего времени даты"
    utils_logger.info('Запуск функции "greetings"')
    try:
        hour = date.hour
        if 6 <= hour <= 11:
            return "Доброе утро"
        elif 12 <= hour <= 17:
            return "Добрый день"
        elif 18 <= hour <= 23:
            return "Добрый вечер"
        elif 0 <= hour <= 5:
            return "Доброй ночи"
    except AttributeError as e:
        utils_logger.error(f"Введено некорректное время: {date}. Ошибка: {str(e)} в функции greetings")
        print("Время не определено")


def filter_operations(df_operations: pd.DataFrame, first_date: datetime, last_date: datetime) -> list[dict | None]:
    "Функция выборки необходимых операций по картам с общей суммой расходов"
    utils_logger.info('Запуск функции "filter_operations"')
    df_status_ok = df_operations[(df_operations["Статус"] == "OK") & (df_operations["Сумма платежа"] <= 0)]
    df_in_date = df_status_ok[
        (df_status_ok["Дата операции"] >= first_date) & (df_status_ok["Дата операции"] <= last_date)
    ]
    df_card_number = df_in_date.groupby("Номер карты")
    summ_price_by_card = df_card_number["Сумма платежа"].sum()
    return summ_price_by_card


def read_excel_file() -> pd.DataFrame | None:
    "Функция чтения Excel-файла"
    utils_logger.info('Запуск функции "read_excel_file"')
    try:
        with open(PATH_OPERATIONS, "rb") as excel_file:
            utils_logger.info('Прочитан файл в функции "read_excel_file"')
            df = pd.read_excel(excel_file)
            df = df.where(pd.notnull(df), None)
            df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
            return df
    except (FileNotFoundError, PermissionError) as e:
        utils_logger.error(f"Ошибка при чтении файла {PATH_OPERATIONS}: {str(e)} в функции read_excel_file")
        print(f"Ошибка при чтении файла {PATH_OPERATIONS}: {str(e)}")


def top_5_transactions(df_operations: pd.DataFrame, first_date: datetime, last_date: datetime) -> list[dict | None]:
    "Функция выборки топ 5 транзакций по сумме операции"
    utils_logger.info('Запуск функции "top_5_transactions"')
    df_status_ok = df_operations[df_operations["Статус"] == "OK"]
    df_in_date = df_status_ok[
        (df_status_ok["Дата операции"] >= first_date) & (df_status_ok["Дата операции"] <= last_date)
    ]
    df_top_5 = df_in_date.sort_values(by="Сумма операции с округлением", ascending=False)
    return df_top_5.head(5).reset_index()


def get_exchange_rate(currency: str) -> float:
    "Функция получения курса валюты"
    utils_logger.info('Запуск функции "get_exchange_rate"')
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{currency}"
        response = requests.get(url, timeout=10)
        utils_logger.info('response ответ получен в функции "get_exchange_rate"')

        return response.json()["rates"]["RUB"]
    except requests.exceptions.RequestException as e:
        utils_logger.error(f"Ошибка API: {e} в функции get_exchange_rate")
        print(f"Ошибка API: {e}")
    except (KeyError, TypeError) as e:
        utils_logger.error(f"Ошибка данных транзакции: {e} в функции get_exchange_rate")
        print(f"Ошибка данных транзакции: {e}")


def get_stocks_price(stock: str) -> float:
    "Функция получения стоимости акции"
    utils_logger.info('Запуск функции "get_stocks_price"')
    try:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key}"
        response = requests.get(url, timeout=10)
        utils_logger.info('response ответ получен в функции "get_stocks_price"')

        return round(float(response.json()["Global Quote"]["05. price"]), 2)
    except requests.exceptions.RequestException as e:
        utils_logger.error(f"Ошибка API: {e} в функции get_stocks_price")
        print(f"Ошибка API: {e}")
    except (KeyError, TypeError) as e:
        utils_logger.error(f"Ошибка данных транзакции: {e} в функции get_stocks_price")
        print(f"Ошибка данных транзакции: {e}")


# if __name__ == "__main__":
#     print(top_5_transactions(read_excel_file(), '2021-12-01 14:12:12', '2021-12-12 14:12:12'))
#     print(find_beginning_date(date_str_in_date('2024-12-12 14:12:12')))
#     print(get_exchange_rate("usd"))
#     print(get_stocks_price("googl"))
