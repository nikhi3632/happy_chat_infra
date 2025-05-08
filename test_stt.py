import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

BEAM_TOKEN = os.environ['BEAM_TOKEN']

url = "https://faster-whisper-base-db92dd5.app.beam.cloud"
headers = {
    'Authorization': f"Bearer {BEAM_TOKEN}"
}

response = requests.post(url + "/warmup", headers=headers)
print(response.status_code, response.headers)

# --- Faster Whisper Request ---
with open("payload.json", "r") as f:
    payload_data = json.load(f)

response_whisper = requests.post(
    url,
    headers={
        "Authorization": f"Bearer {BEAM_TOKEN}",
        "Content-Type": "application/json"
    },
    json=payload_data
)

print("Faster Whisper response:")
print(response_whisper.json())
print(response_whisper.json().keys()) # dict_keys(['text']
