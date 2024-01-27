import platform
from dotenv import load_dotenv
import os

if platform.system == 'linux':
    load_dotenv()
else:
    load_dotenv('../env/dev/.env')

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

SECRET_AUTH = os.environ.get("SECRET_AUTH")