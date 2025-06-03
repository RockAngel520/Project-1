import datetime
import pandas as pd
from config import PATH_OPERATIONS, PATH_SETTINGS


def date_str_in_date(date_str: str) -> datetime:
    "Функция перевода входящего строкового значения даты в дату"
    try:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return date
    except (ValueError) as e:
        print("Дата указана неверно. Правильный формат даты YYYY-MM-DD HH:MM:SS")


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


def filter_operations(df_operations: pd.DataFrame) -> list[dict | None]:
    "Функция выборки необходимых операций"
    df_status_ok = df_operations[df_operations["Статус"] == "OK"]
    df_card_number = df_status_ok.groupby("Номер карты")
    summ_price_by_card = df_card_number["Сумма платежа"].sum()
    return summ_price_by_card
    # return df.to_dict(orient="records")


def read_excel_file() -> pd.DataFrame:
    "Функция чтения Excel-файла"
    try:
        with open(PATH_OPERATIONS, "rb") as excel_file:
            df = pd.read_excel(excel_file)
            df = df.where(pd.notnull(df), None)
            return df
    except (FileNotFoundError, PermissionError) as e:
        print(f"Ошибка при чтении файла {PATH_OPERATIONS}: {str(e)}")
        return []



if __name__ == "__main__":
    print(filter_operations(read_excel_file()))
    # print(greetings(date_str_in_date('2024-12-12 14:12:12')))
