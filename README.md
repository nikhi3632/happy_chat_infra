# happy_chat_infra

[beam.cloud](https://www.beam.cloud/)

```bash
Python 3.12.8
git clone https://github.com/nikhi3632/happy_chat_infra.git
python3.12 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
beam configure <TOKEN>
```

```bash
cd /happy_chat_infra/stt
beam deploy speech2text.py:stt

cd /happy_chat_infra/tts
python upload.py 
beam deploy text2speech.py:tts
```

```bash
cd /happy_chat_infra

curl -X POST 'https://faster-whisper-base-db92dd5-v1.app.beam.cloud' \
-H 'Connection: keep-alive' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <TOKEN>' \
--data @payload.json

curl -X POST 'https://coqui-xtts-v2-0ce9c9b-v1.app.beam.cloud' \
-H 'Connection: keep-alive' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{
    "text": "Hello, this is XTTS speaking.",
    "language": "en",
    "speaker": "Andrew Chipper"
}'
```

```bash
beam volume list
```