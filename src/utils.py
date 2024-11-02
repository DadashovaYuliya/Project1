import datetime
import json
import os
import pandas as pd
import requests
from typing import Any

from dotenv import load_dotenv

load_dotenv()


def greeting() -> str:
    """Фукнция, приветствующая пользователя в зависимости от времени суток"""
    current_date_time = datetime.datetime.now()
    date_string = int(current_date_time.strftime("%H"))
    if 6 <= date_string < 12:
        message = "Доброе утро"
    elif 12 <= date_string < 18:
        message = "Добрый день"
    elif 18 <= date_string < 24:
        message = "Добрый вечер"
    else:
        message = "Доброй ночи"
    return message


def cards(data: str, path: Any) -> list:
    """Функция, формирующая информацию по карте (номер, расход, кэшбэк)"""
    try:
        date_string = datetime.datetime.strptime(data, "%Y-%m-%d %H:%M:%S").date()
        start_date = date_string.replace(day=1)
        reader = pd.read_excel(path, engine="openpyxl")
        reader["Дата операции"] = reader["Дата операции"].apply(
            lambda x: datetime.datetime.strptime(f"{x}", "%d.%m.%Y %H:%M:%S").date()
        )
        filter_param = reader.loc[
            (reader["Номер карты"].notnull())
            & (reader["Статус"] != "FAILED")
            & (reader["Сумма операции"] < 0)
            & (reader["Дата операции"] <= date_string)
            & (reader["Дата операции"] >= start_date)
        ]
        result = filter_param.groupby(["Номер карты"], as_index=False).agg({"Сумма операции": "sum"})
        result["Номер карты"] = result["Номер карты"].apply(lambda x: x.replace("*", ""))
        result["Сумма операции"] = abs(result["Сумма операции"])
        result["Кэшбэк"] = result["Сумма операции"].apply(lambda x: round(x / 100, 2))
        return result.to_dict(orient="records")
    except ValueError:
        print("Неверный формат даты!")
        return []


def top_five_transactions(data: str, path: Any) -> list:
    """Функция, возвращающая топ 5 транзакций по сумме платежа"""
    try:
        date_string = datetime.datetime.strptime(data, "%Y-%m-%d %H:%M:%S").date()
        start_date = date_string.replace(day=1)
        reader = pd.read_excel(path, engine="openpyxl")
        reader["Дата операции"] = reader["Дата операции"].apply(
            lambda x: datetime.datetime.strptime(f"{x}", "%d.%m.%Y %H:%M:%S").date()
        )
        filter_param = reader.loc[
            (reader["Номер карты"].notnull())
            & (reader["Статус"] != "FAILED")
            & (reader["Дата операции"] <= date_string)
            & (reader["Дата операции"] >= start_date)
        ]
        sort_transaction = filter_param.sort_values(by=["Сумма операции"], ascending=False)
        result = sort_transaction[0:5]
        new_list = []
        for index, row in result.iterrows():
            new_dict = {
                "date": row["Дата операции"].strftime("%d.%m.%Y"),
                "amount": abs(row["Сумма операции"]),
                "category": row["Категория"],
                "description": row["Описание"],
            }
            new_list.append(new_dict)
        return new_list
    except ValueError:
        print("Неверный формат даты!")
        return []


def course_currency(path: Any) -> list:
    """Функция, возвращающая курс валют"""
    with open(path, encoding="utf-8") as file:
        currency = json.load(file)
        new_list = []
        for i in currency["user_currencies"]:
            get_date = datetime.datetime.now()
            date = get_date.strftime("%Y-%m-%d")
            key = os.getenv("API_KEY_APILAYER")
            headers = {"apikey": key}
            url = f"https://api.apilayer.com/exchangerates_data/{date}?symbols={'RUB'}&base={i}"

            response = requests.request("GET", url, headers=headers)
            result = response.json()
            new_dict = {"currency": i, "rate": result["rates"]["RUB"]}
            new_list.append(new_dict)
        return new_list


def stock_price(path: str) -> list:
    """Функция, возвращающая стоимость акций из S&P 500"""
    with open(path, encoding="utf-8") as file:
        currency = json.load(file)
        new_list = []
        for i in currency["user_stocks"]:
            key = os.getenv("API_KEY_MARKETSTACK")
            headers = key
            querystring = {"symbols": i}
            url = f"https://api.marketstack.com/v1/eod?access_key={headers}"

            response = requests.request("GET", url, params=querystring)
            result = response.json()

            new_dict = {"stock": i, "price": round(result["data"][0]["low"], 2)}
            new_list.append(new_dict)
        return new_list
