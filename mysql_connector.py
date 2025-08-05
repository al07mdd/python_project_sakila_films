# ● mysql_connector.py — подключение к MySQL и функции поиска

import pymysql
from log_writer import log_error
import os
from dotenv import load_dotenv

# конфигурация подключения
load_dotenv()

config = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DB'),
}


def connect_db():
    """Подключение к MySQL."""
    try:
        connection = pymysql.connect(**config)
        return connection
    except pymysql.MySQLError as e:
        print("Ошибка подключения к MySQL.")
        print(f"MySQL Error: {e}")
        log_error("connect_db", str(e))
        return None

# Функция 1
def search_films_by_keyword(connection, keyword, offset):
    """
    Поиск фильмов по части названия.
        :param connection: подключение к БД
        :param keyword: ключевое слово для поиска
        :param offset: смещение для постраничного вывода
        :return: список фильмов (film_id, title, release_year, rating, length)
    """
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT film_id, title, release_year, rating, length
                FROM film
                WHERE title LIKE %s
                ORDER BY title
                LIMIT 10 OFFSET %s;
            """
            search_param = f"%{keyword}%"
            cursor.execute(sql, (search_param, int(offset)))
            return cursor.fetchall()
    except pymysql.MySQLError as e:
        print("Ошибка выполнения запроса поиска фильма по названию.")
        print(f"MySQL Error: {e}")
        log_error("search_films_by_keyword", str(e))
        return None

# Функция 2
def search_films_by_genre_and_years(connection, genre, year_start, year_end, offset):
    """
    Поиск фильмов по жанру и диапазону годов выпуска.
        :param connection: подключение к БД
        :param genre: название жанра
        :param year_start: начальный год
        :param year_end: конечный год
        :param offset: смещение для постраничного вывода
        :return: список фильмов (film_id, title, release_year, genre)
    """
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT f.film_id, f.title, f.release_year, c.name AS genre
                FROM film AS f
                JOIN film_category AS fc ON f.film_id = fc.film_id
                JOIN category AS c ON fc.category_id = c.category_id
                WHERE c.name = %s
                  AND f.release_year BETWEEN %s AND %s
                ORDER BY f.release_year, f.title
                LIMIT 10 OFFSET %s;
            """
            cursor.execute(sql, (genre, year_start, year_end, int(offset)))
            return cursor.fetchall()
    except pymysql.MySQLError as e:
        print("Ошибка выполнения запроса поиска фильмов по жанру и годам.")
        print(f"MySQL Error: {e}")
        log_error("search_films_by_genre_and_years", str(e))
        return None

# Функция 3
def get_all_genres(connection):
    """
    Получить список всех жанров.
        :param connection: подключение к БД
        :return: список названий жанров
    """
    try:
        with connection.cursor() as cursor:
            sql = "SELECT DISTINCT name FROM category ORDER BY name;"
            cursor.execute(sql)
            result = cursor.fetchall()
            return [row[0] for row in result]
    except pymysql.MySQLError as e:
        print("Ошибка получения списка жанров.")
        print(f"MySQL Error: {e}")
        log_error("get_all_genres", str(e))
        return None

# Функция 4
def get_release_year_range(connection):
    """
    Получить минимальный и максимальный год выпуска фильмов.
        :param connection: подключение к БД
        :return: кортеж (min_year, max_year)
    """
    try:
        with connection.cursor() as cursor:
            sql = "SELECT MIN(release_year), MAX(release_year) FROM film;"
            cursor.execute(sql)
            return cursor.fetchone()
    except pymysql.MySQLError as e:
        print("Ошибка получения диапазона годов.")
        print(f"MySQL Error: {e}")
        log_error("get_release_year_range", str(e))
        return None

# Функция 5
def search_films_by_actor(connection, actor_name, offset):
    """
    Поиск фильмов по имени и/или фамилии актёра (без учёта регистра).
        :param connection: подключение к БД
        :param actor_name: строка (имя, фамилия или оба вместе)
        :param offset: смещение для постраничного вывода
        :return: список фильмов (title, release_year, actor_full_name)
    """
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT f.title, f.release_year, CONCAT(a.first_name, ' ', a.last_name) AS actor
                FROM film AS f
                JOIN film_actor AS fa ON f.film_id = fa.film_id
                JOIN actor AS a ON fa.actor_id = a.actor_id
                WHERE UPPER(CONCAT(a.first_name, ' ', a.last_name)) LIKE %s
                ORDER BY f.release_year DESC, f.title
                LIMIT 10 OFFSET %s;
            """
            param = f"%{actor_name.strip().upper()}%"
            cursor.execute(sql, (param, int(offset)))
            return cursor.fetchall()
    except pymysql.MySQLError as e:
        print("Ошибка при поиске фильмов по актёру.")
        print(f"MySQL Error: {e}")
        log_error("search_films_by_actor", str(e))
        return None

# Функция 6
def get_film_count_by_year(connection):
    """
    Получить количество фильмов по годам выпуска.
        :param connection: подключение к БД
        :return: список кортежей (release_year, film_count)
    """
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT release_year, COUNT(*) AS film_count
                FROM film
                GROUP BY release_year
                ORDER BY release_year;
            """
            cursor.execute(sql)
            return cursor.fetchall()
    except pymysql.MySQLError as e:
        print("Ошибка получения статистики по годам.")
        print(f"MySQL Error: {e}")
        log_error("get_film_count_by_year", str(e))
        return None

# Функция 7
def search_films_by_description(connection, keyword, offset):
    """
    Поиск фильмов по ключевому слову в описании.
        :param connection: подключение к БД
        :param keyword: ключевое слово
        :param offset: смещение для постраничного вывода
        :return: список фильмов (title, release_year, description)
    """
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT title, release_year, description
                FROM film
                WHERE description LIKE %s
                ORDER BY title
                LIMIT 10 OFFSET %s;
            """
            search_param = f"%{keyword}%"
            cursor.execute(sql, (search_param, int(offset)))
            return cursor.fetchall()
    except pymysql.MySQLError as e:
        print("Ошибка поиска по описанию.")
        print(f"MySQL Error: {e}")
        log_error("search_films_by_description", str(e))
        return None
