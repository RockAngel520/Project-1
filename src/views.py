# {'Global Quote': {'01. symbol': 'GOOGL', '02. open': '171.3500', '03. high': '172.2050', '04. low': '167.4400', '05. price': '171.7400', '06. volume': '52639911', '07. latest trading day': '2025-05-30', '08. previous close': '171.8600', '09. change': '-0.1200', '10. change percent': '-0.0698%'}}
import json
from config import PATH_SETTINGS

from utils import date_str_in_date, greetings, filter_operations, read_excel_file, find_beginning_date, top_5_transactions, exchange_rate


def json_answer_main(date: str) -> str:

    last_date = date_str_in_date(date)
    first_date = find_beginning_date(last_date)
    greeting_answer = {"greeting": greetings(last_date)}

    operations_answer = []
    operations = filter_operations(read_excel_file(), first_date, last_date).to_dict()
    for key, value in operations.items():
        operations_answer.append({"last_digits": key[-4:], "total_spent": 0-value, "cashback": round(0-value/100, 2)})
    card_answer = {"cards": operations_answer}

    top_transactions_answer = []
    operations = top_5_transactions(read_excel_file(), first_date, last_date)
    for row in range(5):
        top_transactions_answer.append({"date": operations.loc[row, "Дата платежа"],
                                        "amount": operations.loc[row, "Сумма платежа"],
                                        "category": operations.loc[row, "Категория"],
                                        "description": operations.loc[row, "Описание"]})
    top_5_answer = {"top_transactions": top_transactions_answer}

    # currency_exchange_rate = []
    # with open(PATH_SETTINGS) as file:
    #     user_settings = json.load(file)
    # for key in user_settings["user_currencies"]:
    #     currency_exchange_rate.append({"currency": key,
    #                                           "rate": exchange_rate(key)})
    # currency_exchange_rate_answer = {"currency_rates": currency_exchange_rate}

    answer = dict()
    answer.update(greeting_answer)
    answer.update(card_answer)
    answer.update(top_5_answer)
    answer.update(currency_exchange_rate_answer)


    json_answer = json.dumps(answer, ensure_ascii=False, indent=4)
    return json_answer


# if __name__ == "__main__":
#     print(json_answer_main('2021-12-12 14:12:12'))



# {
#   "greeting": "Добрый день",
#   "cards": [
#     {
#       "last_digits": "5814",
#       "total_spent": 1262.00,
#       "cashback": 12.62
#     },
#     {
#       "last_digits": "7512",
#       "total_spent": 7.94,
#       "cashback": 0.08
#     }
#   ],
#   "top_transactions": [
#     {
#       "date": "21.12.2021",
#       "amount": 1198.23,
#       "category": "Переводы",
#       "description": "Перевод Кредитная карта. ТП 10.2 RUR"
#     },
#     {
#       "date": "20.12.2021",
#       "amount": 829.00,
#       "category": "Супермаркеты",
#       "description": "Лента"
#     },
#     {
#       "date": "20.12.2021",
#       "amount": 421.00,
#       "category": "Различные товары",
#       "description": "Ozon.ru"
#     },
#     {
#       "date": "16.12.2021",
#       "amount": -14216.42,
#       "category": "ЖКХ",
#       "description": "ЖКУ Квартира"
#     },
#     {
#       "date": "16.12.2021",
#       "amount": 453.00,
#       "category": "Бонусы",
#       "description": "Кешбэк за обычные покупки"
#     }
#   ],
#   "currency_rates": [
#     {
#       "currency": "USD",
#       "rate": 73.21
#     },
#     {
#       "currency": "EUR",
#       "rate": 87.08
#     }
#   ],
#   "stock_prices": [
#     {
#       "stock": "AAPL",
#       "price": 150.12
#     },
#     {
#       "stock": "AMZN",
#       "price": 3173.18
#     }
#   ]
# }
