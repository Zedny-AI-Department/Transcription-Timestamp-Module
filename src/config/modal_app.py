import modal

faster_whisper_image = (
    modal.Image.from_registry(
        "nvidia/cuda:12.9.1-cudnn-devel-ubuntu20.04", add_python="3.10"
    )
    .env({"DEBIAN_FRONTEND": "noninteractive"})
    .copy_local_dir(local_path="src", remote_path="/root/src")
    .apt_install("tzdata", "ffmpeg", "git", "libmagic1", "libmagic-dev")
    .pip_install(
        "faster-whisper==1.1.1",
        "torch==2.0.1+cu118",
        "torchaudio==2.0.2+cu118",
        "numpy==2.2.6",
        "fastapi==0.115.13",
        "huggingface-hub==0.33.0",
        "humanfriendly==10.0",
        "hydra-core==1.3.2",
        "hyperframe==6.1.0",
        "pydantic==2.11.7",
        "pydantic-core==2.33.2",
        "pydantic-settings==2.10.1",
        "python-dotenv==1.1.1",
        "python-multipart==0.0.20",
        "uvicorn==0.34.3",
        "levenshtein==0.27.1",
        "rapidfuzz==3.13.0",
        "imageio==2.37.0",
        "imageio-ffmpeg==0.6.0",
        "moviepy==2.2.1",
        "pillow==11.3.0",
        "proglog==0.1.12",
        "python-magic==0.4.27",
        "fuzzywuzzy==0.18.0",
        "zstandard==0.23.0",
        extra_index_url="https://download.pytorch.org/whl/cu118",
    )
)

app = modal.App("timestamp_app")

