import json
from datetime import datetime
from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.views import json_answer_main, json_simple_search


# Фикстуры для тестовых данных
@pytest.fixture
def mock_settings():
    return {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "GOOGL"]}


@pytest.fixture
def mock_excel_data():
    return pd.DataFrame(
        {
            "Дата операции": [datetime(2023, 12, 1), datetime(2023, 12, 15)],
            "Статус": ["OK", "OK"],
            "Сумма платежа": [-1000.0, -2000.0],
            "Номер карты": ["1234567890123456", "1234567890123456"],
            "Дата платежа": ["2023-12-01", "2023-12-15"],
            "Категория": ["Еда", "Транспорт"],
            "Описание": ["Покупка продуктов", "Такси"],
        }
    )


# Тесты для json_answer_main
@patch("src.views.open", new_callable=mock_open)
@patch("src.views.json.load")
@patch("src.views.get_stocks_price")
@patch("src.views.get_exchange_rate")
@patch("src.views.top_5_transactions")
@patch("src.views.filter_operations")
@patch("src.views.find_beginning_date")
@patch("src.views.date_str_in_date")
@patch("src.views.read_excel_file")
def test_json_answer_main(
    mock_read_excel,
    mock_date_str,
    mock_find_date,
    mock_filter,
    mock_top5,
    mock_rates,
    mock_stocks,
    mock_json_load,
    mock_file,
    mock_settings,
    mock_excel_data,
):
    # Настройка моков
    mock_read_excel.return_value = mock_excel_data
    mock_date_str.return_value = datetime(2023, 12, 15, 14, 30)
    mock_find_date.return_value = datetime(2023, 12, 1)

    # Мокируем результаты функций
    mock_filter.return_value = pd.Series([-3000.0], index=pd.Index(["1234567890123456"], name="Номер карты"))

    mock_top5.return_value = pd.DataFrame(
        {
            "Дата платежа": ["2023-12-01", "2023-12-15", "2023-12-10", "2023-12-05", "2023-12-20"],
            "Сумма платежа": [-1000.0, -2000.0, -1500.0, -500.0, -3000.0],
            "Категория": ["Еда", "Транспорт", "Развлечения", "Одежда", "Техника"],
            "Описание": ["Продукты", "Такси", "Кино", "Куртка", "Ноутбук"],
        }
    )

    mock_rates.side_effect = [75.5, 85.3]
    mock_stocks.side_effect = [150.25, 2800.50]
    mock_json_load.return_value = mock_settings

    # Вызов функции
    result = json_answer_main("2023-12-15 14:30:00")
    data = json.loads(result)

    # Проверки
    assert "greeting" in data
    assert len(data["cards"]) == 1
    assert data["cards"][0]["last_digits"] == "3456"
    assert data["cards"][0]["total_spent"] == 3000.0
    assert len(data["top_transactions"]) == 5
    assert len(data["currency_rates"]) == 2
    assert len(data["stock_prices"]) == 2


# Тесты для json_simple_search
@patch("src.views.search_word_in_operations")
def test_json_simple_search(mock_search, mock_excel_data):
    # Настройка мока
    test_data = mock_excel_data.copy()
    test_data["Сумма платежа"] = [-1000.0, -2000.0]
    mock_search.return_value = test_data

    # Вызов функции
    result = json_simple_search("продукты")
    data = json.loads(result)

    # Проверки
    assert len(data["search"]) == 2
    assert data["search"][0]["category"] == "Еда"
    assert data["search"][1]["description"] == "Такси"


@patch("src.views.search_word_in_operations", return_value=pd.DataFrame())
def test_json_simple_search_empty(mock_search):
    result = json_simple_search("несуществующее_слово")
    data = json.loads(result)
    assert len(data["search"]) == 0
