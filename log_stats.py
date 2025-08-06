# ● log_stats.py — получение статистики из MongoDB (частые и последние запросы)

from mongo_connector import get_mongo_connection

db = get_mongo_connection()
queries = db["final_project_queries_170225_DETKOV"]
errors = db["final_project_errors_170225_DETKOV"]

def get_most_frequent_queries(limit = 5):
    """
    Получает список самых популярных поисковых запросов из MongoDB.
        :param limit: максимальное количество запросов для вывода (по умолчанию 5)
        :return: список словарей с информацией о запросах, 
                 включая тип запроса, параметры, количество повторов и время последнего использования
    """
    return list(
        queries.aggregate([
            {
                "$group": {
                    "_id": {
                        "query_type": "$query_type",
                        "parameters": "$parameters"
                    },
                    "count": {"$sum": 1},
                    "last_used": {"$max": "$timestamp"}
                }
            },
            {"$sort": {"count": -1}},
            {"$limit": limit}
        ])
    )

def get_last_unique_queries(limit = 5):
    """
    Получает список последних уникальных поисковых запросов из MongoDB.
        :param limit: максимальное количество уникальных запросов (по умолчанию 5)
        :return: список словарей с полями:
            - _id: словарь с типом запроса и параметрами
            - timestamp: время последнего выполнения данного уникального запроса
    """
    return list(
        queries.aggregate([
            {
                "$group": {
                    "_id": {
                        "query_type": "$query_type",
                        "parameters": "$parameters"
                    },
                    "timestamp": {"$max": "$timestamp"}
                }
            },
            {"$sort": {"timestamp": -1}},
            {"$limit": limit}
        ])
    )

def get_last_errors(limit = 5):
    """
    Получает список последних ошибок, записанных в MongoDB.
        :param limit: максимальное количество ошибок для вывода (по умолчанию 5)
        :return: список словарей с информацией об ошибках, 
            источник (source), сообщение (message) и время (timestamp)
    """
    return list(
        errors.find()
        .sort("timestamp", -1)
        .limit(limit)
    )
