# ● mongo_connector.py — подключение к MONGO DB

from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_mongo_connection():
    uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB")
    client = MongoClient(uri)
    return client[db_name]
