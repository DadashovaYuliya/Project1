import json
import logging
import datetime
from typing import Callable, Any, Optional

import pandas as pd
from black import datetime
from dateutil.relativedelta import relativedelta

path = 'G:/Downloads/operations.xlsx'
df_file = pd.read_excel(path, engine="openpyxl")

logger = logging.getLogger("reports")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/reports.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

def log(filename: Any) -> Callable:
    """Декоратор, который логирует работу функции и выводит результат в файл """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs).to_dict(orient="records")
            with open(filename, "w") as f:
                json.dump(result, f, indent=4)
            return result

        return wrapper

    return decorator


def spending_by_category (transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    try:
        logger.info("Начало работы функции")
        transaction_by_category = []
        filter_df = []

        if date:
            end_date = datetime.strptime(date, '%d.%m.%Y')
            start_date = end_date - relativedelta(month=3)
        else:
            end_date = datetime.datetime.now()
            start_date = end_date - relativedelta(month=3)

        logger.info("Фильтрация по категории")
        for i in transactions:
            if i['Категория'] == category:
                transaction_by_category.append(i)

        for i in transaction_by_category:
            if i['Дата платежа'] == 'nan':
                continue
            elif start_date <= datetime.datetime.strptime(str(i['Дата платежа']), '%d.%m.%Y') <= end_date:
                filter_df.append(i['Сумма операции'])

        logger.info("Завершение работы функции")
        result = json.dumps(filter_df, indent=4, ensure_ascii=False)
        return result

    except Exception as ex:
        logger.error(f"Произошла ошибка: {ex}")
        return pd.DataFrame({})
