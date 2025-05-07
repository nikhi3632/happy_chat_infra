import requests
import os
from dotenv import load_dotenv
load_dotenv()

BEAM_TOKEN = os.environ['BEAM_TOKEN']

# --- Coqui XTTS Request ---
xtts_payload = {
    "text": "Hello, this is XTTS speaking.",
    "language": "en",
    "speaker": "Andrew Chipper"
}

response_xtts = requests.post(
    "https://coqui-xtts-v2-0ce9c9b-v1.app.beam.cloud",
    headers={
        "Authorization": f"Bearer {BEAM_TOKEN}",
        "Content-Type": "application/json"
    },
    json=xtts_payload
)

print("\nXTTS response:")
print(response_xtts.json())

