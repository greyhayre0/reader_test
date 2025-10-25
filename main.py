import argparse
from tabulate import tabulate
from utils.report_brand_rating import report_brand_rating


def main():

    parser = argparse.ArgumentParser(
        description="Генератор отчетов по рейтингам товаров"
    )

    parser.add_argument(
        "--files", nargs="+", required=True, help="Список CSV файлов для обработки"
    )

    parser.add_argument(
        "--report", choices=["average-rating"], required=True, help="Тип отчета"
    )

    args = parser.parse_args()

    if not args.files:
        print("Ошибка: Не указаны файлы для обработки")
        return 1

    try:

        if args.report == "average-rating":
            report_data = report_brand_rating(args.files)

            table_data = []
            for item in report_data:
                table_data.append([item["brand"], item["average_rating"]])

            headers = ["brand", "rating"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))

        else:
            print(f"Ошибка: Неизвестный тип отчета {args.report}")
            return 1

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return 1

    return 0


if __name__ == "__main__":
    main()
