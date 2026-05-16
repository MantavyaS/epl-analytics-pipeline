from api.api_client import make_request

url_prem = "/competitions/2021/standings"
file = "json_files/standings.json"
params = {}

make_request(url_prem, file, params)