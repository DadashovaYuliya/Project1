from src.reports import spending_by_category, df_file
from src.services import get_transactions_by_row
from src.views import greeting, cards, top_five_transactions, course_currency, stock_price, get_home_page

# print(greeting())
#
# print(cards('2021-12-02 23:18:06', 'G:/Downloads/operations.xlsx'))
#
# print(top_five_transactions('2019-09-11 20:29:14', 'G:/Downloads/operations.xlsx'))
#
# print(course_currency('user_settings.json'))
#
# print(stock_price('user_settings.json'))

# print(get_home_page('2021-12-02 23:18:00'))

# print(get_transactions_by_row('G:/Downloads/operations.xlsx', 'каршеринг'))
# print(df_file['Дата платежа'])
print(spending_by_category(df_file, 'Каршеринг', '12.12.2021'))
# {'Дата операции': '16.07.2019 16:30:10', 'Дата платежа': '18.07.2019', 'Номер карты': '*7197', 'Статус': 'OK', 'Сумма операции': -49.8, 'Валюта операции': 'RUB', 'Сумма платежа': -49.8, 'Валюта платежа': 'RUB', 'Кэшбэк': nan, 'Категория': 'Супермаркеты', 'MCC': 5411.0, 'Описание': 'SPAR', 'Бонусы (включая кэшбэк)': 0, 'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 49.8}

# https://github.com/lAntonKuznetsovl/course-paper/blob/feature/coursed_paper/src/services.py