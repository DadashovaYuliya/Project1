from typing import Any

import pandas as pd

from src.reports import spending_by_category
from src.services import get_transactions_by_row
from src.views import get_home_page

path = "G:/Downloads/operations.xlsx"
df_file = pd.read_excel(path, engine="openpyxl")


def main(date: str, data_frame: pd.DataFrame) -> Any:
    print(get_home_page(date))
    row = input("Введите слово для поиска\n")
    print(get_transactions_by_row(path, row))
    category = input("Введите категорию для фильтрации транзакций\n")
    print(spending_by_category(data_frame, category, date))


if __name__ == "__main__":
    date_str = input("Введите дату в формате: DD-MM-YYYY HH:MM:SS:\n")
    print(main(date_str, df_file))
