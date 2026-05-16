from api.api_client import make_request

url_topscorer = "/competitions/2021/scorers"
file = "json_files/topscorers.json"
params = {
    "limit": 10,
    "season": 2025
}

make_request(url_topscorer, file, params)