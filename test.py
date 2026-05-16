import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.football-data.org/v4"
API_KEY = os.getenv("API_KEY")

headers = {
    "X-Auth-Token": API_KEY
}

params = {
    "season": 2025,
    "matchday": 1
}

response = requests.get(
    f"{BASE_URL}/competitions/2021/standings",
    headers=headers,
    params=params
)

print(response.url)
print(response.status_code)

data = response.json()

with open("json_files/standings_matchday_1.json", "w") as f:
    json.dump(data, f, indent=4)