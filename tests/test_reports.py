import json
import pytest
import pandas as pd

from src.reports import decorator_with_args, spending_by_category


def test_decorator_with_args(lst_for_tests_csv_xlsx: list[dict]) -> None:
    @decorator_with_args('logs/decorators_mistakes.json')
    def test_spending_by_category() -> float:
        """Функция тестирует декоратор"""
        expected_result = -20000.0

        # Вызов функции и проверка результата
        result = spending_by_category(
            pd.DataFrame(lst_for_tests_csv_xlsx),
            'Переводы',
            "31.10.2021"
        )

        # Сравнение результатов
        assert result == expected_result, f"Ожидалось {expected_result}, но получено {result}"
        return result

    # Проверка, что функция возвращает float
    result = test_spending_by_category()
    assert isinstance(result, float), "Функция должна возвращать float"
