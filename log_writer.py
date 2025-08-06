# ● log_writer.py — запись поисковых запросов и ошибок в MongoDB

from datetime import datetime
from mongo_connector import get_mongo_connection

db = get_mongo_connection()
queries = db["final_project_queries_170225_DETKOV"]
errors = db["final_project_errors_170225_DETKOV"]

# запись логов запросов
def log_search(query_type, parameters, result_count):
    """
    Записывает информацию о поисковом запросе в MongoDB.
        :param query_type: тип запроса (например, "keyword", "genre_year", "actor")
        :param parameters: словарь с параметрами запроса (например, {"keyword": "matrix"})
        :param result_count: количество найденных результатов
        :return: None
    """
    log_entry = {
        "query_type": query_type,
        "parameters": parameters,
        "result_count": result_count,
        "timestamp": datetime.now()
    }
    try:
        queries.insert_one(log_entry)
    except Exception as e:
        log_error("log_search", str(e))

# запись ошибок
def log_error(source, message):
    """
    Записывает информацию об ошибке в MongoDB.
        :param source: название функции или компонента, где произошла ошибка
        :param message: текст сообщения об ошибке
        :return: None
    """
    error_entry = {
        "source": source,
        "message": message,
        "timestamp": datetime.now()
    }
    try:
        errors.insert_one(error_entry)
    except:
        pass  
    