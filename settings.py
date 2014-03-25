from os import environ
from pymongo import MongoClient


db = MongoClient(environ.get("DB_URL"))["playlist"]
