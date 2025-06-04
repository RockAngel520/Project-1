from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.services import search_word_in_operations


# Фикстура для тестовых данных
@pytest.fixture
def mock_excel_data():
    return pd.DataFrame(
        {
            "Описание": ["Платеж Газпромбанк", "Оплата Такси", "Перевод в Сбербанк", "Оплата услуг Газпромбанк"],
            "Категория": ["Банк", "Транспорт", "Переводы", "Банк"],
            "Дата платежа": ["2023-01-01"] * 4,
            "Сумма платежа": [-1000.0] * 4,
        }
    )


# Тест успешного поиска
@patch("builtins.open", new_callable=mock_open)
@patch("pandas.read_excel")
def test_search_word_in_operations_success(mock_read_excel, mock_file, mock_excel_data):
    # Настраиваем моки
    mock_read_excel.return_value = mock_excel_data

    # Вызываем функцию
    result = search_word_in_operations("газпромбанк")

    # Проверяем результаты
    assert len(result) == 2
    assert all("газпромбанк" in desc.lower() for desc in result["Описание"])
    assert not result.empty


# Тест отсутствия результатов
@patch("builtins.open", new_callable=mock_open)
@patch("pandas.read_excel")
def test_search_no_results(mock_read_excel, mock_file, mock_excel_data):
    mock_read_excel.return_value = mock_excel_data

    result = search_word_in_operations("несуществующееслово")

    assert result.empty


# Тест обработки ошибок файла
@patch("builtins.open", side_effect=FileNotFoundError)
def test_search_word_file_error(mock_file, caplog):
    result = search_word_in_operations("тест")

    assert result is None
    assert "Ошибка при чтении файла" in caplog.text


# Тест регистронезависимого поиска
@patch("builtins.open", new_callable=mock_open)
@patch("pandas.read_excel")
def test_case_insensitive_search(mock_read_excel, mock_file, mock_excel_data):
    mock_read_excel.return_value = mock_excel_data

    result_lower = search_word_in_operations("газпромбанк")
    result_upper = search_word_in_operations("ГАЗПРОМБАНК")
    result_mixed = search_word_in_operations("ГазпромБанк")

    assert len(result_lower) == len(result_upper) == len(result_mixed) == 2
