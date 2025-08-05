# ● formatter.py — функции форматирования вывода (таблицы)

from prettytable import PrettyTable

def print_film_results_table(results):
    """ Вывод списка фильмов в виде таблицы (название, год, рейтинг, длительность). """
    if not results:
        print("Нет данных для отображения.")
        return

    table = PrettyTable()
    table.field_names = ["Название", "Год", "Рейтинг", "Длительность (мин.)"]
    table.align["Название"] = "l"
    table.align["Рейтинг"] = "l"

    for row in results:
        table.add_row(row)

    print(table)


def print_genre_results_table(data):
    """Вывод результатов поиска по жанру и годам (название, год, жанр)"""
    if not data:
        print("Нет данных для отображения.")
        return

    table = PrettyTable()
    table.field_names = ["Название", "Год", "Жанр"]
    table.align["Название"] = "l"

    for title, year, genre in data:
        table.add_row([title, year, genre])

    print(table)

def print_actor_results_table(data):
    """Вывод результатов поиска по актёру (название, год, актёр)"""
    if not data:
        print("Нет данных для отображения.")
        return

    table = PrettyTable()
    table.field_names = ["Название", "Год", "Актёр"]
    table.align["Название"] = "l"
    table.align["Актёр"] = "l"

    for title, year, actor in data:
        table.add_row([title, year, actor])

    print(table)

def print_description_results_table(data):
    """Вывод результатов поиска по описанию (название, год, описание)"""
    if not data:
        print("Нет данных для отображения.")
        return

    table = PrettyTable()
    table.field_names = ["Название", "Год", "Описание"]
    table.align["Название"] = "l"
    table.align["Описание"] = "l"
    table.max_width["Описание"] = 100

    for title, year, description in data:
        table.add_row([title, year, description])

    print(table)

def print_genre_and_year_info(genres, year_range):
    """Вывод списка жанров (4 столбца) и диапазона годов."""
    if not genres:
        print("Жанры не найдены.")
    else:
        print("\nДоступные жанры:")
        genres_sorted = sorted(genres)
        col_width = max(len(g) for g in genres_sorted) + 4

        for i in range(0, len(genres_sorted), 4):
            g1 = genres_sorted[i]
            g2 = genres_sorted[i + 1] if i + 1 < len(genres_sorted) else ''
            g3 = genres_sorted[i + 2] if i + 2 < len(genres_sorted) else ''
            g4 = genres_sorted[i + 3] if i + 3 < len(genres_sorted) else ''
            print(f"- {g1.ljust(col_width)}- {g2.ljust(col_width)}- {g3.ljust(col_width)}- {g4}")

    if not year_range or len(year_range) != 2:
        print("\nДиапазон лет недоступен.")
    else:
        min_year, max_year = year_range
        print(f"\nДиапазон годов выпуска фильмов: {min_year} - {max_year}")

from prettytable import PrettyTable

def print_latest_queries_table(results):
    """Вывод 5 последних уникальных запросов."""
    if not results:
        print("Нет данных.")
        return

    table = PrettyTable()
    table.field_names = ["Тип запроса", "Параметры", "Время"]
    table.align["Тип запроса"] = "l"
    table.align["Параметры"] = "l"

    for item in results:
        query_type = item["_id"]["query_type"]
        params = item["_id"]["parameters"]
        ts = item["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        table.add_row([query_type, str(params), ts])

    print("Последние 5 уникальных запросов:")
    print(table)

def print_error_log_table(errors):
    """Вывод последних 5 ошибок."""
    if not errors:
        print("Нет ошибок в журнале.")
        return

    table = PrettyTable()
    table.field_names = ["Время", "Источник", "Сообщение"]
    table.align["Источник"] = "l"
    table.align["Сообщение"] = "l"
    table.max_width["Сообщение"] = 60

    for err in errors:
        ts = err.get("timestamp", "N/A")
        ts_str = ts.strftime("%Y-%m-%d %H:%M:%S") if hasattr(ts, 'strftime') else str(ts)
        source = err.get("function", err.get("source", "неизвестно"))
        msg = err.get("message", "")
        table.add_row([ts_str, source, msg])

    print("Последние 5 ошибок:")
    print(table)

def print_top_queries_table(results):
    """Вывод топ-5 популярных запросов."""
    if not results:
        print("Нет данных.")
        return

    table = PrettyTable()
    table.field_names = ["Тип запроса", "Параметры", "Частота"]
    table.align["Тип запроса"] = "l"
    table.align["Параметры"] = "l"

    for item in results:
        query_type = item["_id"]["query_type"]
        params = item["_id"]["parameters"]
        count = item["count"]
        table.add_row([query_type, str(params), count])

    print("ТОП 5 популярных запросов:")
    print(table)
