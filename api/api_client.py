import requests, json, os
from dotenv import load_dotenv

load_dotenv()

API_KEY=os.getenv("API_KEY")
URL=os.getenv("BASE_URL")

headers  ={
    "X-Auth-Token": API_KEY
}

def make_request(url_add, file):
    response = requests.get(URL + url_add, headers=headers)
    data = response.json()

    with open(file, "w") as f:
        json.dump(data, f, indent=4)