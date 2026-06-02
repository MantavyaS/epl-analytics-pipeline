import psycopg2
import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

CURR_STANDINGS_FILE = Path("cleaned_json_files/cleaned_standings.json")
PAST_STANDINGS_FILE = Path("cleaned_json_files/cleaned_past_standings.json")
TOPSCORERS_FILE = Path("cleaned_json_files/cleaned_topscorers.json")

with open(CURR_STANDINGS_FILE, "r") as c:
    curr_standings = json.load(c)

with open(PAST_STANDINGS_FILE, "r") as p:
    past_standings = json.load(p)

with open(TOPSCORERS_FILE, "r") as t:
    topscorers = json.load(t)

conn = psycopg2.connect(
    dbname = os.getenv("DB_NAME"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    host = os.getenv("DB_HOST"),
    port = os.getenv("DB_PORT")
)
cur = conn.cursor()

for row in curr_standings:
    cur.execute("""
    INSERT INTO rolling_standings(
            season, matchday, position, team_id, team_name,
            short_name, tla, crest_link, played, won, draw, loss,
            points, goals_for, goals_against, goal_difference
        )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (season, matchday, team_id) DO NOTHING;
    """, (
        row["season"],
        row["matchday"],
        row["position"],
        row["team_id"],
        row["team_name"],
        row["short_name"],
        row["tla"],
        row["crest_link"],
        row["played"],
        row["won"],
        row["draw"],
        row["loss"],
        row["points"],
        row["goals_for"],
        row["goals_against"],
        row["goal_difference"]
    ))

for row in past_standings:
    cur.execute("""
    INSERT INTO rolling_standings(
            season, matchday, position, team_id, team_name,
            short_name, tla, crest_link, played, won, draw, loss,
            points, goals_for, goals_against, goal_difference
        )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (season, matchday, team_id) DO NOTHING;
    """, (
        row["season"],
        row["matchday"],
        row["position"],
        row["team_id"],
        row["team_name"],
        row["short_name"],
        row["tla"],
        row["crest_link"],
        row["played"],
        row["won"],
        row["draw"],
        row["lost"],
        row["points"],
        row["goals_for"],
        row["goals_against"],
        row["goal_difference"]
    ))

for row in topscorers:
    cur.execute("""
    INSERT INTO topscorers (
        season, matchday, player_id, player_name, 
        nationality, team_id, team_name, matches_played,
        goals_scored, assists, penalties
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (season, matchday, player_id) DO NOTHING;
    """, (
        row["season"],
        row["matchday"],
        row["player_id"],
        row["player_name"],
        row["nationality"],
        row["team_id"],
        row["team_name"],
        row["matches_played"],
        row["goals_scored"],
        row["assists"],
        row["penalties"]
    ))

cur.execute("""
SELECT matchday, COUNT(*)
FROM rolling_standings
GROUP BY matchday
ORDER BY matchday;
""")

conn.commit()
cur.close()
conn.close()