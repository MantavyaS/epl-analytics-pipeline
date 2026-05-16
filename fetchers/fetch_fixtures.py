from api.api_client import make_request

file = "raw_json_files/fixtures.json"
url_fixtures = "/competitions/2021/matches"
params = {}

make_request(url_fixtures, file, params)