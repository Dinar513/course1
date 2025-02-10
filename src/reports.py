import json
import os
from datetime import datetime
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta


def decorator_with_args(file: str):
    """Декоратор с параметром, который записывает результаты в указанный файл."""
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


def decorator_without_args(func):
    """Декоратор без параметра, который записывает результаты в файл с именем по умолчанию."""
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            # Генерируем имя файла на основе текущей даты и времени
            default_file = f"logs/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            os.makedirs(os.path.dirname(default_file), exist_ok=True)
            with open(default_file, "w", encoding="utf-8") as file:
                json.dump(result.to_dict("records"), file, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка при записи файла: {e}")
        return result  # Возвращаем результат даже при ошибке
    return wrapper


@decorator_with_args('logs/decorators_mistakes.json')
@decorator_without_args
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