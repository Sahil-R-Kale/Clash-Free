from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()
DB_CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING")
COLLECTION_NAME = os.environ.get("COLLECTION_NAME")

def connect_to_db():
    uri = DB_CONNECTION_STRING
    client = MongoClient(uri)
    collection = client['timetable'][COLLECTION_NAME]
    return collection


