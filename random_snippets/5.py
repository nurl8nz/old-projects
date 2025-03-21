import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
DATABASE = os.getenv("DB_DATABASE")
SERVER_IP = os.getenv("SERVER_IP")

CHECK_FIO_URL = os.getenv("CHECK_FIO_URL")
OMILIA_URL = os.getenv("OMILIA_URL")
BUFFER_URL = os.getenv("BUFFER_URL")

USER_NAME = os.getenv("USER_NAME")
PASS_WORD = os.getenv("PASS_WORD")


DB_CONFIG = {
    'user': USER,
    'password': PASSWORD,
    'host': HOST,
    'database': DATABASE,
    'buffered': True,
    "ssl_disabled": True
}

LOGS_DIRECTORY = 'logs/'
LOGS_BACKUP_DIRECTORY = 'logs/backups/'
