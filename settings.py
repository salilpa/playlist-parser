from os import environ
from pymongo import MongoClient


db = MongoClient(environ.get("DB_URL"))["playlist"]
PER_PAGE = 15
DEVELOPER_KEY = environ.get("DEVELOPER_KEY")

EMAIL = environ.get("EMAIL")
PASS = environ.get("PASS")
PROJECT_URL = environ.get("PROJECT_URL")

url = 'https://www.codeship.io/users/sign_in'
password_field = 'user_password'
email_field = 'user_email'
button = 'signin'
wait_box = 'notice'
class_name = 'branch'
id_name = 'older'
name = 'master'
url_class = 'view'