from api.api_client import make_request

url_topscorer = "/competitions/2021/scorers?limit=10&season=2025"
file = "json_files/topscorers.json"

make_request(url_topscorer, file)