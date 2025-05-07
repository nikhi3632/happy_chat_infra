# happy_chat_infra

[BEAM WEBSITE](https://www.beam.cloud/)

```bash
Python 3.12.8
git clone https://github.com/nikhi3632/happy_chat_infra.git
python3.12 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
beam configure <TOKEN>

cd /happy_chat_infra/stt
beam deploy speech2text.py:stt

cd /happy_chat_infra/tts
python upload.py 
beam deploy text2speech.py:tts
```
