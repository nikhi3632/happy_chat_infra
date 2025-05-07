
from beam import endpoint, Image, Volume, env
import base64
import io

BEAM_VOLUME_PATH = "./cached_models"

# These packages will be installed in the remote container
if env.is_remote():
    from TTS.api import TTS

# This runs once when the container first starts
def load_models():
    model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
    model = TTS(model_name)
    model.to("cuda")
    return model


@endpoint(
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
            "torchaudio",
        ]
    )
    .with_envs([
        "HF_HOME=./cached_models",
        "HF_HUB_ENABLE_HF_TRANSFER=1",
        "COQUI_TOS_AGREED=1"
        ]),
    volumes=[
        Volume(
            name="cached_models",
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

        return {
            "text": text,
            "audio_base64": audio_base64
        }

    except Exception as e:
        return {"error": f"Something went wrong: {e}"}
