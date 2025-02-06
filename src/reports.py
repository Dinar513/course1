import json
import os
from datetime import datetime
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta


def decorator_with_args(file: str):
    """Функция, которая записыват результаты """
    def my_big_decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                os.makedirs(os.path.dirname(file), exist_ok=True)
                with open(file, "w", encoding="utf-8") as file_2:
                    json.dump(result.to_dict("records"), file_2, ensure_ascii=False)
            except Exception as e:
                print(f"Ошибка при записи файла: {e}")
            return result  # Возвращаем результат даже при ошибке
        return wrapper
    return my_big_decorator


@decorator_with_args('logs/decorators_mistakes.json')
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = str(datetime.now())) -> float:
    """Функция, которая возвращает датафрейм с тратами по заданной категории
       за последние три месяца (от переданной даты)."""
    transactions_by_category = transactions[
        (transactions['Дата операции'] <= (pd.to_datetime(date, dayfirst=True) + relativedelta(months=2))) &
        (transactions['Дата операции'] >= pd.to_datetime(date, dayfirst=True)) &
        (transactions['Категория'].str.upper() == category.upper())
        ]

    # Суммируем траты по категории
    total_spending = transactions_by_category['Сумма операции'].sum()

    return total_spending