from .reader import read_csv


def report_brand_rating(file_paths):
    """
    Создает отчет со средним рейтингом по брендам
    """

    data = read_csv(file_paths)

    brand_ratings = {}

    for row in data:
        try:
            brand = row["brand"]
            rating = float(row["rating"])

            if brand not in brand_ratings:
                brand_ratings[brand] = []

            brand_ratings[brand].append(rating)

        except (KeyError, ValueError):

            continue

    results = []
    for brand, ratings in brand_ratings.items():
        average_rating = sum(ratings) / len(ratings)
        results.append({"brand": brand, "average_rating": round(average_rating, 2)})

    results.sort(key=lambda x: x["average_rating"], reverse=True)

    return results
