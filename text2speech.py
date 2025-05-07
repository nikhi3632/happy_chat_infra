
from beam import endpoint, Image, Volume, env, task_queue
import base64
import io
import os

BEAM_VOLUME_PATH = "./cached_tts_models"

# These packages will be installed in the remote container
if env.is_remote():
    from TTS.api import TTS

# This runs once when the container first starts
def load_models():
    try:
        os.makedirs("./cached_tts_models", exist_ok=True)
        model = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=True).to("cuda")
        print("Model loaded successfully!")
        return model
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        raise

@endpoint(
    timeout=600,
    on_start=load_models,
    name="xtts-v2",
    cpu=2,
    memory="32Gi",
    gpu="A10G",
    image=Image(
        base_image="nvidia/cuda:12.4.1-devel-ubuntu22.04", 
        python_version="python3.12"
    )
    .add_python_packages(
        [
            "spacy==3.7.5",
            "pydantic==2.11.4",
            "huggingface_hub[hf-transfer]",
            "huggingface_hub[hf_xet]",
            "ctranslate2",
            "coqui-tts",
            "torchaudio"
        ]
    )
    .with_envs([
        "TTS_HOME=./cached_tts_models",
        "COQUI_TOS_AGREED=1"
        ]),
    volumes=[
        Volume(
            name="cached_tts_models",
            mount_path=BEAM_VOLUME_PATH,
        )
    ],
)
def tts(context, **inputs):
    # Retrieve cached model from on_start
    model : TTS = context.on_start_value

    # Inputs
    text = inputs.get("text")
    language = inputs.get("language")
    if language is None:
        language = 'en'
    speaker = inputs.get("speaker")
    if speaker is None:
        speaker = 'Andrew Chipper'

    if not text:
        return {"error": "Missing required 'text' input."}

    try:
        audio_buffer = io.BytesIO()
        model.tts_to_file(text=text, file_path=audio_buffer, speaker=speaker, language=language)
        audio_buffer.seek(0)

        # Encode to base64
        audio_base64 = base64.b64encode(audio_buffer.read()).decode("utf-8")

        response = {
            "text": text,
            "audio_base64": audio_base64
        }
        print(response)
        return response

    except Exception as e:
        return {"error": f"Something went wrong: {e}"}
