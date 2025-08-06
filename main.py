# ● main.py — точка входа, меню и обработка команд пользователя

import matplotlib.pyplot as plt

from mysql_connector import (
    connect_db,
    search_films_by_keyword,
    search_films_by_genre_and_years,
    get_all_genres,
    get_release_year_range,
    search_films_by_actor,
    get_film_count_by_year,
    search_films_by_description )
from log_writer import (log_search, log_error)
from log_stats import (get_most_frequent_queries, get_last_unique_queries, get_last_errors)
from formatter import (
    print_film_results_table,
    print_genre_results_table,
    print_actor_results_table,
    print_description_results_table,
    print_genre_and_year_info,
    print_top_queries_table,
    print_latest_queries_table,
    print_error_log_table
)

def main_menu():
    """ Запускает главное меню консольного приложения.
            Функция обрабатывает ввод пользователя и предоставляет доступ к:
            - поиску фильмов,
            - статистике запросов,
            - выходу из программы.
        :return: None (управление осуществляется через цикл while)
    """
    connection = connect_db()
    if not connection:
        print("Программа завершена из-за ошибки подключения.")
        log_error("main_menu", "Программа завершена из-за ошибки подключения.")
        return
    
    while True:
        print("\nГЛАВНОЕ МЕНЮ:")
        print('--- Меню ---')
        print('"0". Выход')
        print('"1". Поиск фильмов')
        print('"2". Статистика запросов')

        choice = input("Выберите действие: ").strip()

        if choice == "0":
            print("До свидания!")
            connection.close()
            break
        elif choice == "1":
            menu_films(connection)
        elif choice == "2":
            menu_stats()
        else:
            print("Некорректный ввод. Попробуйте снова.")


def menu_films(connection):
    """ Отображает подменю поиска фильмов и обрабатывает выбор пользователя.
        :param connection: подключение к базе данных MySQL
        :return: None 
    """
    while True:
        print("\nПОИСК ФИЛЬМОВ:")
        print('"0". Назад в главное меню')
        print('"1". Поиск фильмов по ключевому слову')
        print('"2". Поиск фильмов по жанру и диапазону годов')
        print('"3". Поиск фильмов по имени актёра')
        print('"4". Поиск фильмов по описанию')
        print('"5". Количество фильмов по годам (график)')

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            keyword_search(connection)
        elif choice == "2":
            genre_year_search(connection)
        elif choice == "3":
            actor_search(connection)
        elif choice == "4":
            description_search(connection)
        elif choice == "5":
            show_film_stats_by_year(connection)
        elif choice == "0":
            print("\nДо свидания!")
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")


def menu_stats():
    """ Отображает подменю статистики запросов и обрабатывает выбор пользователя.
        :return: None 
    """
    while True:
        print("\nСТАТИСТИКА ЗАПРОСОВ:")
        print('"0". Назад в главное меню')
        print('"1". ТОП 5 популярных запросов')
        print('"2". Последние 5 уникальных запросов')
        print('"3". Последние 5 ошибок')

        choice = input("Выберите действие: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            show_popular_queries()
        elif choice == "2":
            show_latest_queries()
        elif choice == "3":
            show_last_5_errors()
        else:
            print("Некорректный ввод. Попробуйте снова.")


def keyword_search(connection):
    """ Выполняет поиск фильмов по ключевому слову.
            Пользователь вводит ключевое слово, после чего выводятся результаты постранично (по 10 фильмов).
            По завершении поиска запрос сохраняется в MongoDB.
        :param connection: подключение к базе данных MySQL
        :return: None (результаты выводятся в консоль и логируются)
    """
    keyword = input("Введите ключевое слово для поиска: ").strip()
    if not keyword:
        print("Ключевое слово не может быть пустым.")
        return

    offset = 0
    total_found = 0

    while True:
        results = search_films_by_keyword(connection, keyword, offset)
        if results is None:
            log_error("keyword_search", "Поиск фильмов по ключевому слову = None")
            print("Ошибка при поиске.")
            return
        if not results:
            if offset == 0:
                print("Нет результатов.")
            break

        formatted_results = [(film[1], film[2], film[3], film[4]) for film in results] # название - год - рейтинг - длительность
        print_film_results_table(formatted_results)
        total_found += len(results)

        next_action = input("\nПоказать следующие 10? (y/n): ").strip().lower()
        if next_action == 'y':
            offset += 10
        else:
            break

    log_search("keyword", {"keyword": keyword}, total_found)        # запись поисковых логов


def genre_year_search(connection):
    """ Поиск фильмов по жанру и диапазону годов выпуска.
        Пользователь выбирает жанр из доступного списка и указывает начальный и конечный год
        (можно ввести только один год для поиска за конкретный год).
            валидация ввода:
            - проверка существования жанра,
            - проверка, что год является числом,
            - проверка, что годы входят в допустимый диапазон,
            - не допускает, чтобы конечный год был меньше начального,
            - проверяет, что год состоит максимум из 4 цифр.
        Результаты выводятся постранично (по 10 фильмов).
        По завершении поиска запрос сохраняется в MongoDB.
        :param connection: подключение к базе данных MySQL
        :return: None (результаты выводятся в консоль и логируются)
    """
    genres = get_all_genres(connection)
    if not genres:
        log_error("genre_year_search", "Список жанров = None")
        print("Не удалось получить список жанров.")
        return

    year_range = get_release_year_range(connection)
    if not year_range:
        log_error("genre_year_search", "Диапазон годов = None")
        print("Не удалось получить диапазон годов.")
        return

    print_genre_and_year_info(genres, year_range)

    # обработка ввода жанра
    genre_input = input("Введите название жанра: ").strip().lower()
    genres_map = {g.lower(): g for g in genres}

    if genre_input not in genres_map:
        print("Некорректный жанр.")
        return

    genre = genres_map[genre_input]  # безопасное имя жанра для SQL запроса

    try:
        year_start_input = input(f"Начальный год ({year_range[0]} - {year_range[1]}): ").strip()
        year_end_input = input(
            f"Конечный год ({year_range[0]} - {year_range[1]}), "
            f"или Enter для поиска только по {year_start_input}: "
        ).strip()

        year_start = int(year_start_input)
        year_end = int(year_end_input) if year_end_input else year_start

    except ValueError as e:
        log_error("genre_year_search", f"ValueError при вводе года: {e}")
        print("Ошибка: год должен быть числом.")
        return

    # проверка логики ввода годов выпуска
    for label, year in [("Начальный год", year_start), ("Конечный год", year_end)]:
        if len(str(year)) > 4:
            msg = f"Год состоит более чем из 4 цифр: {label.lower()}={year}"
            log_error("genre_year_search", msg)
            print("Год должен состоять максимум из 4 цифр.")
            return
        if year < year_range[0] or year > year_range[1]:
            msg = f"{label} {year} вне диапазона {year_range[0]} - {year_range[1]}"
            log_error("genre_year_search", msg)
            print(f"{label} должен быть в диапазоне {year_range[0]} - {year_range[1]}.")
            return

    if year_end < year_start:
        msg = f"Конечный год {year_end} меньше начального года {year_start}"
        log_error("genre_year_search", msg)
        print("Конечный год не может быть меньше начального.")
        return

    offset = 0
    total_found = 0

    while True:
        results = search_films_by_genre_and_years(connection, genre, year_start, year_end, offset)
        if results is None:
            log_error("genre_year_search", "Поиск фильмов по жанру и диапазону годов = None")
            print("Ошибка при поиске.")
            return
        if not results:
            if offset == 0:
                print("Нет результатов.")
            break

        formatted = [(f[1], f[2], f[3]) for f in results]  # название - год - жанр
        print_genre_results_table(formatted)
        total_found += len(results)

        next_action = input("\nПоказать следующие 10? (y/n): ").strip().lower()
        if next_action == 'y':
            offset += 10
        else:
            break

    # запись поисковых логов
    log_search("genre_year", {
        "genre": genre,
        "year_start": year_start,
        "year_end": year_end
    }, total_found)


def actor_search(connection):
    """ Поиск фильмов по имени и/или фамилии актёра (без учёта регистра).
            Пользователь вводит часть имени или фамилии актёра, результаты выводятся постранично (по 10 фильмов).
            По завершении поиска запрос сохраняется в MongoDB.
        :param connection: подключение к базе данных MySQL
        :return: None (результаты выводятся в консоль и логируются)
    """
    actor_input = input("Введите имя, фамилию актера или их часть: ").strip()
    if not actor_input:
        print("Имя актёра не может быть пустым.")
        return

    offset = 0
    total_found = 0

    while True:
        results = search_films_by_actor(connection, actor_input, offset)
        if results is None:
            log_error("actor_search", "Поиск фильмов по имени актёра = None")
            print("Ошибка при поиске актёра.")
            return
        if not results:
            if offset == 0:
                print("Фильмы не найдены.")
            break

        formatted = [(f[0], f[1], f[2]) for f in results] # название - год - актерк
        print_actor_results_table(formatted)    
        total_found += len(results)

        next_action = input("\nПоказать следующие 10? (y/n): ").strip().lower()
        if next_action == 'y':
            offset += 10
        else:
            break

    log_search("actor", {"actor_name": actor_input}, total_found)       # запись поисковых логов


def description_search(connection):
    """ Поиск фильмов по ключевому слову в описании.
            Пользователь вводит ключевое слово, результаты выводятся постранично (по 10 фильмов).
            По завершении поиска запрос сохраняется в MongoDB.
        :param connection: подключение к базе данных MySQL
        :return: None (результаты выводятся в консоль и логируются)
    """
    keyword = input("Введите ключевое слово из описания: ").strip()
    if not keyword:
        print("Ключевое слово не может быть пустым.")
        return

    offset = 0
    total_found = 0

    while True:
        results = search_films_by_description(connection, keyword, offset)
        if results is None:
            log_error("description_search", "Поиск фильмов по ключевому слову в описании = None")
            print("Ошибка при выполнении по ключевому слову в описании.")
            return
        if not results:
            if offset == 0:
                print("Ничего не найдено.")
            break

        formatted = [(f[0], f[1], f[2]) for f in results] # название - год - описание
        print_description_results_table(formatted)
        total_found += len(results)

        next_action = input("\nПоказать следующие 10? (y/n): ").strip().lower()
        if next_action == 'y':
            offset += 10
        else:
            break

    log_search("description", {"keyword": keyword}, total_found)    # запись поисковых логов


def show_film_stats_by_year(connection):
    """ Отображает график количества фильмов по годам выпуска.
            Данные берутся из MySQL и строятся с помощью matplotlib.
        :param connection: подключение к базе данных MySQL
        :return: None (результат отображается в виде графика)
    """
    data = get_film_count_by_year(connection)
    if data is None:
        log_error("show_film_stats_by_year", "Отображение графика количества фильмов по годам = None")
        print("Не удалось получить данные.")
        return
    if not data:
        print("Нет данных для отображения.")
        return

    years = [row[0] for row in data]
    counts = [row[1] for row in data]

    plt.figure(figsize=(10, 5))
    plt.plot(years, counts, marker='o')
    plt.title("Количество фильмов по годам")
    plt.xlabel("Год выпуска")
    plt.ylabel("Количество фильмов")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def show_popular_queries():
    """ Отображает ТОП-5 популярных поисковых запросов из MongoDB.
            Данные извлекаются функцией get_most_frequent_queries()
            и выводятся в виде таблицы.
        :return: None (результаты печатаются в консоль)
    """  
    results = get_most_frequent_queries()
    if not results:
        print("Нет данных.")
        return
    print_top_queries_table(results)


def show_latest_queries():
    """ Отображает последние 5 уникальных поисковых запросов из MongoDB.
            Данные извлекаются функцией get_last_unique_queries()
            и выводятся в виде таблицы.
        :return: None (результаты печатаются в консоль)
    """
    results = get_last_unique_queries()
    if not results:
        print("Нет данных.")
        return
    print_latest_queries_table(results)


def show_last_5_errors():
    """ Отображает последние 5 ошибок из MongoDB.
            Данные извлекаются функцией get_last_errors()
            и выводятся в виде таблицы.
        :return: None (информация отображается в консоли)
    """
    errors = get_last_errors(limit = 5)
    if not errors:
        print("Нет ошибок в журнале.")
        return
    print_error_log_table(errors)


if __name__ == "__main__":
    try:
        main_menu()
    except Exception as e:
        print("Произошла критическая ошибка.")
        log_error("main_menu", str(e))
