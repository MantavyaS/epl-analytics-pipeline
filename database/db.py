import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

try:
    conn = get_connection()    
    cur = conn.cursor()

    cur.execute("""SELECT current_database();""")

    print("Connected successfully!")
    print("Database:", cur.fetchone()[0])

    cur.execute("""
    CREATE TABLE IF NOT EXISTS rolling_standings (
        season INTEGER,
        matchday INTEGER,
        position INTEGER,
        team_id INTEGER,
        team_name TEXT,
        short_name TEXT,
        tla VARCHAR(3),
        crest_link TEXT,
        played INTEGER,
        won INTEGER,
        draw INTEGER,
        loss INTEGER,
        points INTEGER,
        goals_for INTEGER,
        goals_against INTEGER,
        goal_difference INTEGER,
        PRIMARY KEY (season, matchday, team_id)
        );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS topscorers (
    season INTEGER,
    matchday INTEGER,
    player_id INTEGER,
    player_name TEXT,
    nationality TEXT,
    team_id INTEGER,
    team_name TEXT,
    matches_played INTEGER,
    goals_scored INTEGER,
    assists INTEGER,
    penalties INTEGER,
    PRIMARY KEY (season, matchday, player_id)
    )
    """)

    conn.commit()
    cur.close()
    conn.close()

except Exception as e:
    print("Connection failed:")
    print(e)