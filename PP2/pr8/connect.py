import psycopg2
from config import DB_CONFIG

def get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("Connected to PostgreSQL successfully!")
        return conn
    except Exception as e:
        print(f"Connection error: {e}")
        return None

if __name__ == "__main__":
    conn = get_connection()
    if conn:
        conn.close()
        