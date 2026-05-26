import json
from pathlib import Path

RAW_FILE = Path("raw_json_files/topscorers.json")
OUTPUT_FILE = Path("cleaned_json_files/cleaned_topscorers.json")

with open(RAW_FILE, "r") as r:
    raw = json.load(r)

cleaned_rows = []

season = raw["filters"]["season"]
matchday = raw["season"]["currentMatchday"]

for player in raw["scorers"]:
    cleaned_row = {
        "season": season,
        "matchday": matchday,
        "player_id": player["player"]["id"],
        "player_name": player["player"]["name"],
        "nationality": player["player"]["nationality"],
        "team_id": player["team"]["id"],
        "team_name": player["team"]["name"],
        "matches_played": player["playedMatches"],
        "goals_scored": player["goals"],
        "assists": player["assists"],
        "penalties": player["penalties"]
    }

    cleaned_rows.append(cleaned_row)

with open(OUTPUT_FILE, "w") as o:
    json.dump(cleaned_rows, o, indent=4)



