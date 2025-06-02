import datetime


def date_str_in_date(date_str: str) -> datetime:
    try:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return date
    except (ValueError) as e:
        print("Дата указана неверно. Правильный формат даты YYYY-MM-DD HH:MM:SS")
        return []


def greetings(date) -> None:
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
        return []






if __name__ == "__main__":
    print(greetings(date_str_in_date('2024-12-12 вв:12:12')))
