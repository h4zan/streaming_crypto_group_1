import os
from dotenv import load_dotenv

load_dotenv()

COINMARKET_API = os.getenv("COINMARKET_API")
EXCHANGE_RATE_API = os.getenv("EXCHANGE_RATE_API")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DBNAME = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
