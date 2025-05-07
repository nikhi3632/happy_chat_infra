# happy_chat_infra

[BEAM WEBSITE](https://www.beam.cloud/)

```bash
Python 3.12.8
git clone https://github.com/nikhi3632/happy_chat_infra.git
python3.12 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
beam configure <TOKEN>
beam serve transcribe_app.py:transcription
beam serve output_app.py:output
```
