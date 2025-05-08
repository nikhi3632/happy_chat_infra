import requests
import os
from dotenv import load_dotenv
load_dotenv()

BEAM_TOKEN = os.environ['BEAM_TOKEN']
TTS_DEPLOYMENT_ID = os.environ['TTS_DEPLOYMENT_ID']

url = f"https://coqui-xtts-v2-{TTS_DEPLOYMENT_ID}.app.beam.cloud"
headers = {
    'Authorization': f"Bearer {BEAM_TOKEN}"
}

response = requests.post(url + "/warmup", headers=headers)
print(response.status_code, response.headers)

# --- Coqui XTTS Request ---
xtts_payload = {
    "text": "Hello, this is XTTS speaking.",
    "language": "en",
    "speaker": "Andrew Chipper"
}

response_xtts = requests.post(
    url,
    headers={
        "Authorization": f"Bearer {BEAM_TOKEN}",
        "Content-Type": "application/json"
    },
    json=xtts_payload
)

print("\nXTTS response:")
print(response_xtts.json())

