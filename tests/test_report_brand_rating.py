import pytest
import os
import tempfile
import sys

# Добавляем путь к корневой директории для импорта
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.report_brand_rating import report_brand_rating


def create_test_file(content):
    """Создает временный файл с заданным содержимым"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(content)
        return f.name


class TestAverageRatingReport:
    def test_basic_functionality(self):
        """Тест основной функциональности отчета"""
        content = """name,brand,price,rating
iphone,apple,1000,4.9
galaxy,samsung,800,4.7
iphone2,apple,900,4.8"""

        test_file = create_test_file(content)

        try:
            result = report_brand_rating([test_file])

            # Проверяем количество брендов
            assert len(result) == 2

            # Проверяем правильность вычислений
            apple_rating = next(item for item in result if item["brand"] == "apple")
            samsung_rating = next(item for item in result if item["brand"] == "samsung")

            assert apple_rating["average_rating"] == 4.85  # (4.9 + 4.8) / 2
            assert samsung_rating["average_rating"] == 4.7

            # Проверяем сортировку (по убыванию рейтинга)
            assert result[0]["average_rating"] >= result[1]["average_rating"]

        finally:
            os.unlink(test_file)

    def test_multiple_files(self):
        """Тест отчета по нескольким файлам"""
        content1 = """name,brand,price,rating
iphone,apple,1000,4.9"""

        content2 = """name,brand,price,rating
galaxy,samsung,800,4.7
iphone2,apple,900,4.8"""

        file1 = create_test_file(content1)
        file2 = create_test_file(content2)

        try:
            result = report_brand_rating([file1, file2])

            # Должен объединить данные из обоих файлов
            assert len(result) == 2

            apple_rating = next(item for item in result if item["brand"] == "apple")
            assert apple_rating["average_rating"] == 4.85  # (4.9 + 4.8) / 2

        finally:
            os.unlink(file1)
            os.unlink(file2)

    def test_invalid_rating_data(self):
        """Тест обработки некорректных данных рейтинга"""
        content = """name,brand,price,rating
product1,brand1,100,not_a_number
product2,brand2,200,4.5
product3,brand3,300,6.0"""

        test_file = create_test_file(content)

        try:
            result = report_brand_rating([test_file])

            # Должен обработать только валидные данные
            assert len(result) == 2

            brands = [item["brand"] for item in result]
            assert "brand1" not in brands  # Пропущен из-за ошибки
            assert "brand2" in brands
            assert "brand3" in brands

        finally:
            os.unlink(test_file)

    def test_missing_columns(self):
        """Тест файла с отсутствующими колонками"""
        content = """name,company,cost,score
product1,comp1,100,5.0"""

        test_file = create_test_file(content)

        try:
            result = report_brand_rating([test_file])

            # Не должно быть данных, т.к. нет колонок brand и rating
            assert len(result) == 0

        finally:
            os.unlink(test_file)

    def test_single_rating_per_brand(self):
        """Тест когда у бренда только один рейтинг"""
        content = """name,brand,price,rating
product1,apple,100,5.0
product2,samsung,200,4.5"""

        test_file = create_test_file(content)

        try:
            result = report_brand_rating([test_file])

            assert len(result) == 2
            assert result[0]["average_rating"] == 5.0
            assert result[1]["average_rating"] == 4.5

        finally:
            os.unlink(test_file)

    def test_empty_data(self):
        """Тест когда нет валидных данных"""
        content = """name,brand,price,rating
product1,brand1,100,invalid
product2,brand2,200,not_number"""

        test_file = create_test_file(content)

        try:
            result = report_brand_rating([test_file])
            assert len(result) == 0

        finally:
            os.unlink(test_file)
