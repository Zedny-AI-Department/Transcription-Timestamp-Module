from ast import Bytes
import io
import os
import tempfile
from typing import BinaryIO
from moviepy import VideoFileClip


async def convert_video_to_audio(video_bytes: Bytes, video_name: str) -> BinaryIO:
    """
    Converts a video file to an audio file. 

    Args:
        video_file (str): The path to the video file.

    Returns:
        BinaryIO: The audio file as a BinaryIO object.   
    """
    try:
        # Save video temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{video_name.split('.')[-1]}") as temp_video:
            temp_video.write(video_bytes)
            temp_video_path = temp_video.name

        # Load video and extract audio using moviepy
        video_clip = VideoFileClip(temp_video_path)
        temp_audio_path = temp_video_path.replace(f".{video_name.split('.')[-1]}", ".wav")
        video_clip.audio.write_audiofile(temp_audio_path, codec='pcm_s16le')  # WAV format

        # Read audio back into BinaryIO
        audio_binary = io.BytesIO()
        with open(temp_audio_path, "rb") as f:
            audio_binary.write(f.read())
        audio_binary.seek(0)

        # Cleanup temporary files
        os.remove(temp_audio_path)
        os.remove(temp_video_path)
        
        return audio_binary
    except Exception as e:
        raise Exception(f"An error occurred while converting video to audio: {e}")
