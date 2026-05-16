from api.api_client import make_request

file = "json_files/fixtures.json"
url_fixtures = "/competitions/2021/matches"

make_request(url_fixtures, file)