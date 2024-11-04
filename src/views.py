import json
from typing import Any

from src.utils import cards, course_currency, greeting, stock_price, top_five_transactions


def get_home_page(data: str) -> Any:
    """Функция, выводящая главную страницу по дате"""

    result = {
        "greeting": greeting(),
        "cards": cards(data, "G:/Downloads/operations.xlsx"),
        "top_transactions": top_five_transactions(data, "G:/Downloads/operations.xlsx"),
        "currency_rates": course_currency("user_settings.json"),
        "stock_prices": stock_price("user_settings.json"),
    }
    result_json = json.dumps(result, indent=4, ensure_ascii=False)
    return result_json
