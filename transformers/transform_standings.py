import json
from pathlib import Path

RAW_FILE = Path("raw_json_files/standings.json")
OUTPUT_FILE = Path("cleaned_json_files/cleaned_standings.json")

with open(RAW_FILE, "r") as r:
    raw = json.load(r)

cleaned_rows = []

season = raw["filters"]["season"]
matchday = raw["season"]["currentMatchday"]

table = raw["standings"][0]["table"]

for team in table:
    cleaned_row = {
        "season": season,
        "matchday": matchday,
        
        "position": team["position"],

        "team_id": team["team"]["id"],
        "team_name": team["team"]["name"],
        "short_name": team["team"]["shortName"],
        "tla": team["team"]["tla"],
        "crest_link": team["team"]["crest"],

        "played": team["playedGames"],
        "won": team["won"],
        "draw": team["draw"],
        "loss": team["lost"],

        "points": team["points"],
        "goals_for": team["goalsFor"],
        "goals_against": team["goalsAgainst"],
        "goal_difference": team["goalDifference"]
    }
    
    cleaned_rows.append(cleaned_row)

with open(OUTPUT_FILE, "w") as o:
    json.dump(cleaned_rows, o, indent=4)