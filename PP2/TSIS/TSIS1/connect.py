#Without changes
import psycopg2
from psycopg2 import OperationalError
from config import DB_CONFIG


def get_connection():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        return connection
    except OperationalError as e:
        print(f"Connection error: {e}")
        return None