import json
import logging
import pandas as pd
from typing import Any



logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/services.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

def get_transactions_by_row(path: Any, row: str) -> Any:
    """Функция, фильтрующая список транзакций по строке поиска"""
    try:
        logger.info("Чтение транзакций из файла")
        reader = pd.read_excel(path, engine="openpyxl")
        filter_transaction = []
        filter_param = reader.loc[
            (reader["Категория"].notnull())
            & (reader["Описание"].notnull())]
        result = filter_param.to_dict(orient="records")
        try:
            logger.info("Поиск строки в списке транзакций")
            for i in result:
                if row.lower() in str(i.get('Категория').lower() or str(i.get('Описание'))):
                    filter_transaction.append(i)
            result_json = json.dumps(filter_transaction, indent=4, ensure_ascii=False)
            return result_json
        except Exception as ex:
            logger.error(f"Строки в транзакциях не найдено: {ex}")
            return [{}]
    except Exception as ex:
        logger.error(f"Произошла ошибка чтения файла: {ex}")
        return [{}]