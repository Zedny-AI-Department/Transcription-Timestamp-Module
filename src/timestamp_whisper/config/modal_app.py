import modal

faster_whisper_image = (
    modal.Image.from_registry(
        "nvidia/cuda:12.9.1-cudnn-devel-ubuntu20.04", add_python="3.10"
    )
    .env({"DEBIAN_FRONTEND": "noninteractive"})
    .copy_local_dir(local_path="src/config", remote_path="/root/src/config")
    .copy_local_file(local_path="src/utils/video_compression_util.py", remote_path="/root/src/utils/video_compression_util.py")
    .apt_install("tzdata", "ffmpeg", "git")
    .pip_install(
        "faster-whisper==1.1.1",
        "torch==2.0.1+cu118",
        "torchaudio==2.0.2+cu118",
        "numpy==2.2.6",
        "pydantic==2.11.7",
        "pydantic-core==2.33.2",
        "pydantic-settings==2.10.1",
        "python-dotenv==1.1.1",
        "zstandard==0.23.0",
        extra_index_url="https://download.pytorch.org/whl/cu118",
    )
)

app = modal.App("timestamp_app")

