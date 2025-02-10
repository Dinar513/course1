import math
from typing import Any

import pandas as pd

from src.utils import df_to_transactions


def investment_bank(month: str, transactions: list[dict[str, Any]], limit: int) -> float:
    """Функция, которая позволяет задавать комфортный порог округления: 10, 50 или 100 ₽.
     Траты будут округляться, и разница между фактической суммой трат по карте
      и суммой округления будет попадать насчет «Инвесткопилки»."""
    num = 0
    rounded_num = round(num, 2)
    transactions = df_to_transactions(transactions)
    for i in transactions:
        if pd.to_datetime(i['Дата операции']) < pd.to_datetime(month, format='%Y-%m'):
            rounded_num += math.ceil(abs(i['Сумма операции']) / limit) * limit - abs(i['Сумма операции'])
    return rounded_num
