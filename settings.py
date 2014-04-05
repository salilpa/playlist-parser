from os import environ
from pymongo import MongoClient


db = MongoClient(environ.get("DB_URL"))["playlist"]
PER_PAGE = 15
DEVELOPER_KEY = environ.get("DEVELOPER_KEY")