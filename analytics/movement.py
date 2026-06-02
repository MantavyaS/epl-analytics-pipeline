import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

cur = conn.cursor()

try:
    cur.execute("""
    WITH start_end AS (
        SELECT
            team_name,
            FIRST_VALUE(position) OVER (
                PARTITION BY team_name
                ORDER BY matchday ASC
            ) AS start_position,
            FIRST_VALUE(position) OVER (
                PARTITION BY team_name
                ORDER BY matchday DESC
            ) AS end_position
        FROM rolling_standings
        WHERE matchday BETWEEN 33 AND 38
    ),

    position_change AS (
        SELECT DISTINCT
            team_name,
            start_position,
            end_position,
            start_position - end_position AS position_gain
        FROM start_end
    )

    SELECT *
    FROM position_change
    ORDER BY position_gain DESC;
    """)

    results = cur.fetchall()

    print(f"Returned {len(results)} rows")

    for row in results:
        print(row)

except Exception as e:
    print("Error:", e)

finally:
    cur.close()
    conn.close()