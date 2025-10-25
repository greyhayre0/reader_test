import csv


def read_csv(file_paths):
    """
    Читает данные из нескольких CSV файлов
    """
    all_data = []

    for file_path in file_paths:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    all_data.append(row)
        except FileNotFoundError:
            print(f"Ошибка: Файл {file_path} не найден")
            raise
        except Exception as e:
            print(f"Ошибка при чтении файла {file_path}: {e}")
            raise

    return all_data
