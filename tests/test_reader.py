import pytest
import os
import tempfile
import sys

# Добавляем путь к корневой директории для импорта
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.reader import read_csv


def create_test_file(content):
    """Создает временный файл с заданным содержимым"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(content)
        return f.name


class TestFileReader:
    def test_read_single_file(self):
        """Тест чтения одного файла"""
        content = """name,brand,price,rating
iphone,apple,1000,4.9
galaxy,samsung,800,4.7"""

        test_file = create_test_file(content)

        try:
            result = read_csv([test_file])

            # Проверяем количество строк
            assert len(result) == 2

            # Проверяем содержимое
            assert result[0]["brand"] == "apple"
            assert result[0]["rating"] == "4.9"
            assert result[1]["brand"] == "samsung"
            assert result[1]["rating"] == "4.7"

        finally:
            os.unlink(test_file)

    def test_read_multiple_files(self):
        """Тест чтения нескольких файлов"""
        content1 = """name,brand,price,rating
iphone,apple,1000,4.9"""

        content2 = """name,brand,price,rating
galaxy,samsung,800,4.7"""

        file1 = create_test_file(content1)
        file2 = create_test_file(content2)

        try:
            result = read_csv([file1, file2])

            # Проверяем что данные из обоих файлов
            assert len(result) == 2

            brands = [row["brand"] for row in result]
            assert "apple" in brands
            assert "samsung" in brands

        finally:
            os.unlink(file1)
            os.unlink(file2)

    def test_file_not_found(self):
        """Тест ошибки когда файл не найден"""
        with pytest.raises(FileNotFoundError):
            read_csv(["nonexistent_file.csv"])

    def test_empty_file(self):
        """Тест пустого файла (только заголовки)"""
        content = "name,brand,price,rating\n"

        test_file = create_test_file(content)

        try:
            result = read_csv([test_file])
            assert len(result) == 0

        finally:
            os.unlink(test_file)

    def test_file_with_only_headers(self):
        """Тест файла с разными заголовками"""
        content = "product,company,cost,score\nitem1,comp1,100,5.0"

        test_file = create_test_file(content)

        try:
            result = read_csv([test_file])
            # Должен прочитать файл, но не найти нужных колонок
            assert len(result) == 1
            assert "brand" not in result[0]  # Нет колонки brand

        finally:
            os.unlink(test_file)
