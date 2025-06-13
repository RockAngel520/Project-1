from datetime import datetime
from unittest.mock import Mock, patch

import pandas as pd
import pytest
import requests

from src.utils import (date_str_in_date, filter_operations, find_beginning_date, get_exchange_rate, get_stocks_price,
                       greetings, read_excel_file, top_5_transactions)


# Фикстура для тестов с датами
@pytest.fixture
def sample_datetime():
    return datetime(2023, 12, 15, 14, 30, 0)


# Фикстура для тестов с DataFrame
@pytest.fixture
def sample_df():
    data = {
        "Дата операции": ["2023-12-01 10:00:00", "2023-12-10 15:30:00", "2023-12-15 09:45:00"],
        "Статус": ["OK", "FAILED", "OK"],
        "Сумма платежа": [-1000, 500, -2000],
        "Сумма операции с округлением": [-1000, 500, -2000],
        "Номер карты": ["1234", "5678", "1234"],
    }
    df = pd.DataFrame(data)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"])
    return df


# Тесты для date_str_in_date
def test_date_str_in_date_valid():
    result = date_str_in_date("2023-12-15 14:30:00")
    assert result == datetime(2023, 12, 15, 14, 30)


# Тесты для find_beginning_date
def test_find_beginning_date(sample_datetime):
    result = find_beginning_date(sample_datetime)
    assert result == datetime(2023, 12, 1, 0, 0, 0)


# Тесты для greetings
@pytest.mark.parametrize(
    "year, month, day, hour, minute, greeting",
    [
        (2023, 1, 1, 8, 0, "Доброе утро"),
        (2023, 1, 1, 14, 0, "Добрый день"),
        (2023, 1, 1, 20, 0, "Добрый вечер"),
        (2023, 1, 1, 2, 0, "Доброй ночи"),
    ],
)
def test_greetings(year, month, day, hour, minute, greeting):
    assert greetings(datetime(year, month, day, hour, minute)) == greeting


def test_greetings_invalid(caplog):
    assert greetings("not-a-datetime") is None
    assert "Введено некорректное время" in caplog.text


# Тесты для filter_operations
def test_filter_operations(sample_df):
    first_date = datetime(2023, 12, 1)
    last_date = datetime(2023, 12, 15)
    result = filter_operations(sample_df, first_date, last_date)
    assert len(result) == 1  # Только одна карта с операциями
    assert result["1234"] == -1000  # Сумма по карте 1234


# Тесты для read_excel_file
@patch("builtins.open")
@patch("pandas.read_excel")
def test_read_excel_file_success(mock_read_excel, mock_open):
    mock_read_excel.return_value = pd.DataFrame({"Дата операции": ["2023-12-01"]})
    result = read_excel_file()
    assert isinstance(result, pd.DataFrame)


@patch("builtins.open", side_effect=FileNotFoundError)
def test_read_excel_file_failure(mock_open, caplog):
    result = read_excel_file()
    assert result is None
    assert "Ошибка при чтении файла" in caplog.text


# Тесты для top_5_transactions
def test_top_5_transactions(sample_df):
    first_date = datetime(2023, 12, 1)
    last_date = datetime(2023, 12, 15)
    result = top_5_transactions(sample_df, first_date, last_date)
    assert len(result) == 1  # Только 2 успешные операции
    assert result.iloc[0]["Сумма операции с округлением"] == -1000


# Тесты для get_exchange_rate
@patch("requests.get")
def test_get_exchange_rate_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"rates": {"RUB": 90.5}}
    mock_get.return_value = mock_response

    result = get_exchange_rate("USD")
    assert result == 90.5


@patch("requests.get", side_effect=requests.exceptions.RequestException)
def test_get_exchange_rate_failure(mock_get, caplog):
    result = get_exchange_rate("USD")
    assert result is None
    assert "Ошибка API" in caplog.text


# Тесты для get_stocks_price
@patch("requests.get")
def test_get_stocks_price_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"Global Quote": {"05. price": "135.25"}}
    mock_get.return_value = mock_response

    result = get_stocks_price("GOOGL")
    assert result == 135.25


@patch("requests.get", side_effect=requests.exceptions.RequestException)
def test_get_stocks_price_failure(mock_get, caplog):
    result = get_stocks_price("GOOGL")
    assert result is None
    assert "Ошибка API" in caplog.text
