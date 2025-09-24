import requests
import dotenv
import os
import json

dotenv.load_dotenv()

JAMENDO_CLIENT_ID = os.getenv("JAMENDO_CLIENT_ID")
name = "Let Me Hear You I"


r = requests.get(
    f"https://api.jamendo.com/v3.0/tracks/?client_id={JAMENDO_CLIENT_ID}&format=jsonpretty&limit=2&namesearch={name}&",
)

with open("jamendo.json", "w") as f:
    json.dump(r.json(), f)
