import requests, json, os
from dotenv import load_dotenv

load_dotenv()

API_KEY=os.getenv("API_KEY")
URL=os.getenv("BASE_URL")

headers  ={
    "X-Auth-Token": API_KEY
}

def make_request(url_add, file, params):
    response = requests.get(
        URL + url_add,
        headers=headers,
        params=params
    )
    response.raise_for_status()
    
    data = response.json()

    with open(file, "w") as f:
        json.dump(data, f, indent=4)