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
            FIRST_VALUE(points) OVER (
                PARTITION BY team_name
                ORDER BY matchday ASC
            ) AS start_points,
            FIRST_VALUE(points) OVER (
                PARTITION BY team_name
                ORDER BY matchday DESC
            ) AS end_points
        FROM rolling_standings
        WHERE matchday BETWEEN 33 AND 38
    )
    SELECT DISTINCT 
        team_name,
        start_points,
        end_points,
        end_points - start_points as points_gained
    FROM start_end
    ORDER BY points_gained DESC
    """)

    results = cur.fetchall()

    for row in results:
        print(row)

except Exception as e:
    print("Error:", e)

cur.close()
conn.close()