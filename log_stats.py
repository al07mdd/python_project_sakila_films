# ● log_stats.py — получение статистики из MongoDB (частые и последние запросы)

from mongo_connector import get_mongo_connection

db = get_mongo_connection()
queries = db["final_project_queries_170225_DETKOV"]
errors = db["final_project_errors_170225_DETKOV"]

def get_most_frequent_queries(limit = 5):
    """ Вывод 5 самых популярных запросов """
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
    """ Вывод 5 последних уникальных запросов """
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
    """ Получение ошибок работы программы """
    return list(
        errors.find()
        .sort("timestamp", -1)
        .limit(limit)
    )
