import datetime
import json
import logging
from typing import Any, Callable, Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

path = "G:/Downloads/operations.xlsx"
df_file = pd.read_excel(path, engine="openpyxl")

logger = logging.getLogger("reports")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/reports.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def log(filename: Any) -> Callable:
    """Декоратор, который логирует работу функции и выводит результат в файл"""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs).to_dict(orient="records")
            with open(filename, "w") as f:
                json.dump(result, f, indent=4)
            return result

        return wrapper

    return decorator


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> str:
    try:
        logger.info("Начало работы функции")
        if date is None:
            end_date = datetime.datetime.now()

        else:
            end_date = datetime.datetime.strptime(date, "%d-%m-%Y %H:%M:%S")

        start_date = end_date - relativedelta(months=3)
        df_date = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")
        filter_category = transactions[(start_date <= df_date) & (df_date <= end_date)]

        logger.info("Фильтрация по категории")
        result_dict = {
            "Категория": category,
            "Расходы по категории": float(round(filter_category["Сумма операции"].sum(), 2)),
            "Дата начала": start_date.strftime("%Y-%m-%d"),
            "Дата конца": end_date.strftime("%Y-%m-%d"),
        }

        if not result_dict["Расходы по категории"]:
            logger.info("По выбранной категории не было трат в заданный период")
            message = "По выбранной категории не было трат в заданный период"
            return message
        logger.info("Конец работы функции")
        result_json = json.dumps(result_dict, indent=4, ensure_ascii=False)
        return result_json

    except Exception as ex:
        logger.error(f"Произошла ошибка: {ex}")
        message = "Произошла ошибка. Проверьте вводимые данные."
        return message
