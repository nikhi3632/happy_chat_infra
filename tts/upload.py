from beam import function, Volume, Image, env

if env.is_remote():
    from huggingface_hub import snapshot_download

VOLUME_PATH = "./cached_tts_models"

@function(
    image=Image(python_version="python3.12")
    .add_python_packages(["huggingface_hub", "huggingface_hub[hf-transfer]"])
    .with_envs([
        "COQUI_TOS_AGREED=1",
        "HF_HUB_ENABLE_HF_TRANSFER=1"
        ]),
    memory="32Gi",
    cpu=4,
    secrets=["HF_TOKEN"],
    volumes=[Volume(name="cached_tts_models", mount_path=VOLUME_PATH)],
)
def upload():
    snapshot_download(
        repo_id="coqui/XTTS-v2", local_dir=f"{VOLUME_PATH}/coqui-xtts-v2"
    )

    print("Files uploaded successfully")


if __name__ == "__main__":
    upload()
