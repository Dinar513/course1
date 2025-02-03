import json

import pandas as pd

from src.reports import decorator_with_args, spending_by_category


def test_decorator_with_args(lst_for_tests_csv_xlsx: list[dict]) -> None:
    @decorator_with_args('logs/decorators_mistakes.json')
    def test_spending_by_category() -> pd.DataFrame:
        """Функция тестирует декоратор"""
        expected_data = [{'Сумма операции': -20000.0}]

        # Вызов функции и проверка результата
        result_df = spending_by_category(
            pd.DataFrame(lst_for_tests_csv_xlsx),
            'Переводы',
            "31.10.2021"
        )

        # Сравнение результатов
        assert result_df.to_dict("records") == expected_data
        return result_df

        # Проверка, что функция возвращает DataFrame

    result = test_spending_by_category()
    assert isinstance(result, pd.DataFrame), "Функция должна возвращать DataFrame"