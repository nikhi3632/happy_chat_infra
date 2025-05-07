import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

BEAM_TOKEN = os.environ['BEAM_TOKEN']

# --- Faster Whisper Request ---
with open("payload.json", "r") as f:
    payload_data = json.load(f)

response_whisper = requests.post(
    "https://faster-whisper-base-db92dd5-v1.app.beam.cloud",
    headers={
        "Authorization": f"Bearer {BEAM_TOKEN}",
        "Content-Type": "application/json"
    },
    json=payload_data
)

print("Faster Whisper response:")
print(response_whisper.json())
