# ● formatter.py — функции форматирования вывода (таблицы)

from prettytable import PrettyTable
from colorama import Fore, Style, init

init(autoreset=True) # сброс цветного форматирования, после каждого print

def print_film_results_table(results):
    """
    Отображает список фильмов в виде таблицы (название, год, рейтинг, длительность).
        :param results: список кортежей (title, release_year, rating, length)
        :return: None (вывод осуществляется в консоль)
    """
    if not results:
        print(Fore.YELLOW + "Нет данных для отображения.")
        return

    print(Fore.YELLOW + "\nРезультаты поиска фильмов:")
    table = PrettyTable()
    table.field_names = ["Название", "Год", "Рейтинг", "Длительность (мин.)"]
    table.align["Название"] = "l"
    table.align["Рейтинг"] = "l"

    for row in results:
        table.add_row(row)

    print(Fore.YELLOW + str(table))


def print_genre_results_table(data):
    """
    Отображает результаты поиска фильмов по жанру и диапазону годов в виде таблицы (название, год, жанр).
        :param data: список кортежей (title, release_year, genre)
        :return: None (результаты выводятся в консоль)
    """
    if not data:
        print(Fore.YELLOW + "Нет данных для отображения.")
        return

    print(Fore.YELLOW + "\nРезультаты поиска фильмов по жанру и диапазону годов:")
    table = PrettyTable()
    table.field_names = ["Название", "Год", "Жанр"]
    table.align["Название"] = "l"

    for title, year, genre in data:
        table.add_row([title, year, genre])

    print(Fore.YELLOW + str(table))


def print_actor_results_table(data):
    """
    Отображает список фильмов, найденных по имени актёра, в виде таблицы (название, год, актёр).
        :param data: список кортежей (title, release_year, actor_full_name)
        :return: None (результаты выводятся в консоль)
    """
    if not data:
        print(Fore.YELLOW + "Нет данных для отображения.")
        return

    print(Fore.YELLOW + "\nРезультаты поиска фильмов с участием актёра:")
    table = PrettyTable()
    table.field_names = ["Название", "Год", "Актёр"]
    table.align["Название"] = "l"
    table.align["Актёр"] = "l"

    for title, year, actor in data:
        table.add_row([title, year, actor])

    print(Fore.YELLOW + str(table))


def print_description_results_table(data):
    """
    Отображает результаты поиска фильмов по ключевому слову в описании в виде таблицы (название, год, описание).
        :param data: список кортежей (title, release_year, description)
        :return: None (результаты выводятся в консоль; описание обрезается до 100 символов)
    """
    if not data:
        print(Fore.YELLOW + "Нет данных для отображения.")
        return

    print(Fore.YELLOW + "\nРезультаты поиска фильмов по описанию:")
    table = PrettyTable()
    table.field_names = ["Название", "Год", "Описание"]
    table.align["Название"] = "l"
    table.align["Описание"] = "l"
    table.max_width["Описание"] = 100

    for title, year, description in data:
        table.add_row([title, year, description])

    print(Fore.YELLOW + str(table))


def print_genre_and_year_info(genres, year_range):
    """
    Отображает список доступных жанров (в 4 колонки) и диапазон годов выпуска фильмов.
        :param genres: список строк с названиями жанров, например ["Action", "Drama", "Comedy"]
        :param year_range: кортеж (min_year, max_year) или None
        :return: None (результаты выводятся в консоль)
    """
    if not genres:
        print(Fore.YELLOW + "Жанры не найдены.")
    else:
        print(Fore.YELLOW + "\nДоступные жанры:")
        genres_sorted = sorted(genres)
        col_width = max(len(g) for g in genres_sorted) + 4

        for i in range(0, len(genres_sorted), 4):
            g1 = genres_sorted[i]
            g2 = genres_sorted[i + 1] if i + 1 < len(genres_sorted) else ''
            g3 = genres_sorted[i + 2] if i + 2 < len(genres_sorted) else ''
            g4 = genres_sorted[i + 3] if i + 3 < len(genres_sorted) else ''
            print(Fore.YELLOW + f"- {g1.ljust(col_width)}- {g2.ljust(col_width)}- {g3.ljust(col_width)}- {g4}")

    if not year_range or len(year_range) != 2:
        print(Fore.YELLOW + "\nДиапазон лет недоступен.")
    else:
        min_year, max_year = year_range
        print(Fore.YELLOW + f"\nДиапазон годов выпуска фильмов: {min_year} - {max_year}")


def print_latest_queries_table(results):
    """
    Отображает последние 5 уникальных поисковых запросов в виде таблицы.
        :param results: список словарей, возвращаемых из MongoDB, где каждый элемент содержит:
        - _id: словарь с ключами "query_type" и "parameters"
        - timestamp: время последнего выполнения запроса (datetime)
        :return: None (результаты выводятся в консоль)
    """
    if not results:
        print(Fore.GREEN + "Нет данных.")
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

    print(Fore.GREEN + "\nПоследние 5 уникальных запросов:")
    print(Fore.GREEN + str(table))


def print_error_log_table(errors):
    """
    Отображает последние 5 ошибок программы в виде таблицы.
        :param errors: список словарей с информацией об ошибках, где каждый словарь может содержать:
        - timestamp: время возникновения ошибки (datetime или строка)
        - source / function: источник или название функции, вызвавшей ошибку
        - message: текст сообщения об ошибке
        :return: None (результаты выводятся в консоль; сообщение обрезается до 60 символов)
    """
    if not errors:
        print(Fore.GREEN + "Нет ошибок в журнале.")
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

    print(Fore.RED + "\nПоследние 5 ошибок:")
    print(Fore.RED + str(table))


def print_top_queries_table(results):
    """
    Отображает топ-5 популярных поисковых запросов в виде таблицы.
        :param results: список словарей, возвращаемых из MongoDB, где каждый элемент содержит:
        - _id: словарь с ключами "query_type" и "parameters"
        - count: количество выполнений данного запроса
        :return: None (результаты выводятся в консоль)
    """
    if not results:
        print(Fore.GREEN + "Нет данных.")
        return

    table = PrettyTable()
    table.field_names = ["Тип запроса", "Параметры", "Частота", "Последний вызов"]
    table.align["Тип запроса"] = "l"
    table.align["Параметры"] = "l"

    for item in results:
        query_type = item["_id"]["query_type"]
        params = item["_id"]["parameters"]
        count = item["count"]
        last_used = item.get("last_used")
        ts_str = last_used.strftime("%Y-%m-%d %H:%M:%S") if last_used else "N/A"
        table.add_row([query_type, str(params), count, ts_str])

    print(Fore.GREEN + "\nТОП 5 популярных запросов:")
    print(Fore.GREEN + str(table))
