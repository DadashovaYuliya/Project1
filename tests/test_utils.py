from unittest.mock import patch

import pandas as pd
import pytest
from freezegun import freeze_time


from src.utils import cards, course_currency, greeting, stock_price, top_five_transactions


def test_greeting():
    """Положительные тесты на приветствие"""
    with freeze_time("2024-11-02 06:15:15"):
        assert greeting() == "Доброе утро"
    with freeze_time("2024-11-02 13:15:15"):
        assert greeting() == "Добрый день"
    with freeze_time("2024-11-02 19:15:15"):
        assert greeting() == "Добрый вечер"
    with freeze_time("2024-11-02 00:15:15"):
        assert greeting() == "Доброй ночи"


@pytest.fixture
def test_df():
    """Фикстура, создающая тестовый DataFrame"""
    test = {
        "Дата операции": [
            "01.12.2021 12:35:05",
            "01.12.2021 13:12:18",
            "01.12.2021 18:50:24",
            "01.12.2021 23:40:34",
            "02.12.2021 14:41:17",
            "02.12.2021 15:18:26",
            "02.12.2021 16:26:02",
            "02.12.2021 21:10:00",
            "02.12.2021 21:44:30",
        ],
        "Номер карты": ["*7197", "*7197", "*7197", "*5091", "*7197", "*7197", "*5091", "*7197", "*5091"],
        "Статус": ["OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK"],
        "Сумма операции": [-99.00, -199.00, -99.22, -1.07, -15.00, -496.51, -5510.80, -125.00, -10.33],
        "Кэшбэк": [None, None, None, None, None, None, None, None, None],
        "Категория": [
            "Фастфуд",
            "Дом и ремонт",
            "Супермаркеты",
            "Каршеринг",
            "Связь",
            "Супермаркеты",
            "Каршеринг",
            "Фастфуд",
            "Каршеринг",
        ],
        "Описание": [
            "IP Yakubovskaya M.V.",
            "Строитель",
            "Дикси",
            "Ситидрайв",
            "Devajs Servis.",
            "Магнит",
            "Ситидрайв",
            "ЦЕХ",
            "Ситидрайв",
        ],
    }

    return pd.DataFrame(test)


# def test_cards(test_df):
#     """Положительный тест вывода информации по карте"""
#     assert cards("2021-12-02 23:18:06", test_df) == [
#         {"Номер карты": "5091", "Сумма операции": 5522.2, "Кэшбэк": 55.22},
#         {"Номер карты": "7197", "Сумма операции": 1033.73, "Кэшбэк": 10.34},
#     ]


def test_cards_no_date(test_df):
    """Тест функции с некорректным форматом даты"""
    assert cards("02.12.2021", test_df) == []


# def test_top_five_transactions(test_df):
#     """Положительный тест вывода топ 5 транзакций"""
#     assert top_five_transactions("2021-12-02 23:18:06", test_df) == [
#         {"date": "01.12.2021", "amount": 1.07, "category": "Каршеринг", "description": "Ситидрайв"},
#         {"date": "02.12.2021", "amount": 10.33, "category": "Каршеринг", "description": "Ситидрайв"},
#         {"date": "02.12.2021", "amount": 15.0, "category": "Связь", "description": "Devajs Servis."},
#         {"date": "01.12.2021", "amount": 99.0, "category": "Фастфуд", "description": "IP Yakubovskaya M.V."},
#         {"date": "01.12.2021", "amount": 99.22, "category": "Супермаркеты", "description": "Дикси"},
#     ]


def test_top_five_transactions_no_date(test_df):
    """Тест функции с некорректным форматом даты"""
    assert cards("02.12.2021", test_df) == []


@patch("src.utils.requests.request")
def test_course_currency(mock_get):
    """Тест на работу конвертации валюты с API"""
    mock_get.return_value.json.return_value = {
        "date": "2018-02-22",
        "historical": "",
        "rates": {"RUB": 50.00, "timestamp": 1519328414},
        "query": {"amount": 10, "from": "USD", "to": "RUB"},
        "result": 50.00,
        "success": True,
    }
    assert course_currency("C:/Users/ddm24/PycharmProjects/Project1/data/test.json") == [
        {"currency": "USD", "rate": 50.0}
    ]


@patch("src.utils.requests.request")
def test_stock_price(mock_get):
    """Тест на работу получения стоимости акций с API"""
    mock_get.return_value.json.return_value = {"data": [{"low": 127.75, "timestamp": 1519328414}]}
    assert stock_price("C:/Users/ddm24/PycharmProjects/Project1/data/test.json") == [
        {"stock": "AAPL", "price": 127.75}
    ]
