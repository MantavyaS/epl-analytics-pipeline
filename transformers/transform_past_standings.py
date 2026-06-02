import json
from pathlib import Path 

OUTPUT_FILE = Path("cleaned_json_files/cleaned_past_standings.json")
all_cleaned_rows = []
for i in range(33, 38):
    RAW_FILE = Path(f"raw_json_files/matchweek{i}_standings.json")

    with open(RAW_FILE, "r") as r:
        raw = json.load(r)
    
    season = raw["filters"]["season"]
    matchday = raw["filters"]["matchday"]

    table = raw["standings"][0]["table"]
    cleaned_rows = []
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
            "lost": team["lost"],

            "points": team["points"],
            "goals_for": team["goalsFor"],
            "goals_against": team["goalsAgainst"],
            "goal_difference": team["goalDifference"]
        }
        cleaned_rows.append(cleaned_row)
    
    all_cleaned_rows.extend(cleaned_rows)

with open(OUTPUT_FILE, "w") as o:
    json.dump(all_cleaned_rows, o, indent=4)