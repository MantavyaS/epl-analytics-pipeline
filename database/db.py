import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

try:
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

    cur = conn.cursor()

    cur.execute("SELECT current_database();")

    print("Connected successfully!")
    print("Database:", cur.fetchone()[0])

    cur.close()
    conn.close()

except Exception as e:
    print("Connection failed:")
    print(e)