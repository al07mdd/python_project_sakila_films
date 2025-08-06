# ● mongo_connector.py — подключение к MONGO DB

from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_mongo_connection():
    """
    Устанавливает подключение к базе данных MongoDB.
        :return: объект базы данных MongoDB (pymongo.database.Database),
        полученный на основе переменных окружения MONGO_URI и MONGO_DB.
    """    
    uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB")
    client = MongoClient(uri)
    return client[db_name]
