import datetime
import pandas as pd
from config import PATH_OPERATIONS
import requests


def date_str_in_date(date_str: str) -> datetime:
    "Функция перевода входящего строкового значения даты в дату"
    try:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return date
    except (ValueError) as e:
        print("Дата указана неверно. Правильный формат даты YYYY-MM-DD HH:MM:SS")


def find_beginning_date(date_end: datetime) -> datetime:
    "Функция нахождения начального дня фильтрации данных"
    beginning_date = datetime.datetime(date_end.year, date_end.month, 1, 0, 0, 0)
    return beginning_date


def greetings(date) -> str | None:
    "Функция приветствия в зависимости от входящего времени даты"
    try:
        hour = date.hour
        if 6 <= hour <= 11:
            return "Доброе утро"
        elif 12 <= hour <= 17:
            return "Добрый день"
        elif 18 <= hour <= 23:
            return "Добрый вечер"
        elif 0 <= hour <= 5:
            return "Добрый день"
    except (AttributeError) as e:
        print("Время не определено")


def filter_operations(df_operations: pd.DataFrame, first_date: datetime, last_date: datetime) -> list[dict | None]:
    "Функция выборки необходимых операций по картам с общей суммой расходов"
    df_status_ok = df_operations[(df_operations["Статус"] == "OK") & (df_operations["Сумма платежа"] <= 0)]
    df_in_date = df_status_ok[(df_status_ok["Дата операции"] >= first_date) & (df_status_ok["Дата операции"] <= last_date)]
    df_card_number = df_in_date.groupby("Номер карты")
    summ_price_by_card = df_card_number["Сумма платежа"].sum()
    return summ_price_by_card


def read_excel_file() -> pd.DataFrame | None:
    "Функция чтения Excel-файла"
    try:
        with open(PATH_OPERATIONS, "rb") as excel_file:
            df = pd.read_excel(excel_file)
            df = df.where(pd.notnull(df), None)
            df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
            return df
    except (FileNotFoundError, PermissionError) as e:
        print(f"Ошибка при чтении файла {PATH_OPERATIONS}: {str(e)}")


def top_5_transactions(df_operations: pd.DataFrame, first_date: datetime, last_date: datetime) -> list[dict | None]:
    "Функция выборки топ 5 транзакций по сумме операции"
    df_status_ok = df_operations[df_operations["Статус"] == "OK"]
    df_in_date = df_status_ok[(df_status_ok["Дата операции"] >= first_date) & (df_status_ok["Дата операции"] <= last_date)]
    df_top_5 = df_in_date.sort_values(by="Сумма операции с округлением", ascending=False)
    return df_top_5.head(5).reset_index()


def exchange_rate(currency: str) -> float:
    "Функция получения курса валюты"
    url = f"https://api.exchangerate-api.com/v4/latest/{currency}"
    response = requests.get(url, timeout=10)

    return response.json()["rates"]["RUB"]


def get_stocks_price(stock: str) -> float:
    "Функция получения стоимости акции"
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&month=2009-01&outputsize=full&apikey={}"
    headers = {"apikey": api_key}

    response = requests.get(url, headers=headers, timeout=10)

    return round(response.json()["result"], 2)

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&month=2009-01&outputsize=full&apikey=ZY4PVW7T89RVZBJ5'
r = requests.get(url)
data = r.json()
print(data)


if __name__ == "__main__":
    # print(top_5_transactions(read_excel_file(), '2021-12-01 14:12:12', '2021-12-12 14:12:12'))
    # print(find_beginning_date(date_str_in_date('2024-12-12 14:12:12')))
    print(exchange_rate("usd"))
