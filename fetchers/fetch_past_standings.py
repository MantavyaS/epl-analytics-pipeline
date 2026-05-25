from api.api_client import make_request

url = "/competitions/2021/standings"
first_matchweek = 33
for i in range(5):
    current_matchweek = first_matchweek + i

    params = {
        "season": 2025,
        "matchday": current_matchweek
    }
    file = f"raw_json_files/matchweek{current_matchweek}_standings.json"
    make_request(url, file, params)