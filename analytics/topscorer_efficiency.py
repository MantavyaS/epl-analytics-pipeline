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
    SELECT
        player_name,
        team_name,
        matches_played,
        goals_scored,
        assists,
        ROUND(
            (COALESCE(goals_scored, 0) + COALESCE(assists, 0))::numeric / matches_played, 2
        ) AS goal_contributions_per_game
    FROM topscorers
    WHERE matches_played > 0
    ORDER BY goal_contributions_per_game DESC;
    """)

    results = cur.fetchall()

    for row in results:
        print(row)

except Exception as e:
    print("Error:", e)

cur.close()
conn.close()