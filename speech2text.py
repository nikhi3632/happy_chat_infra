
from beam import endpoint, Image, Volume, env
import base64
import io

BEAM_VOLUME_PATH = "./cached_models"

# These packages will be installed in the remote container
if env.is_remote():
    from faster_whisper import WhisperModel, download_model


# This runs once when the container first starts
def load_models():
    model_path = download_model("base", cache_dir=BEAM_VOLUME_PATH)
    model = WhisperModel(model_path, device="cuda", compute_type="float16")
    return model


@endpoint(
    on_start=load_models,
    name="faster-whisper",
    cpu=2,
    memory="32Gi",
    gpu="A10G",
    image=Image(
        base_image="nvidia/cuda:12.8.1-cudnn-runtime-ubuntu22.04",
        python_version="python3.12",
    )
    .add_python_packages(
        [
            "git+https://github.com/SYSTRAN/faster-whisper.git",
            "huggingface_hub[hf-transfer]",
            "huggingface_hub[hf_xet]",
            "faster-whisper",
            "ctranslate2",
        ]
    )
    .with_envs("HF_HUB_ENABLE_HF_TRANSFER=1"),
    volumes=[
        Volume(
            name="cached_models",
            mount_path=BEAM_VOLUME_PATH,
        )
    ],
)
def stt(context, **inputs):
    # Retrieve cached model from on_start
    model : WhisperModel = context.on_start_value

    # Inputs
    language = inputs.get("language")
    if language is None:
        language = 'en'
    audio_base64 = inputs.get("audio_file")

    if not audio_base64:
        return {"error": "Missing required 'audio_file' in base64 format."}

    try:
        # Decode base64 to binary audio data
        binary_data = base64.b64decode(audio_base64.encode("utf-8"))
        audio_stream = io.BytesIO(binary_data)

        # Transcribe
        segments, _ = model.transcribe(audio_stream, language=language)
        text = " ".join(segment.text for segment in segments)
        return {"text": text}

    except Exception as e:
        return {"error": f"Something went wrong: {e}"}
