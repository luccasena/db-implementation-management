import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
OPEN_F1_API_BASE_URL = os.getenv("OPEN_F1_API_BASE_URL")