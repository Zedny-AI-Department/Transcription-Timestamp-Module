from typing import BinaryIO, List, Union
from faster_whisper import WhisperModel

from src.models.transcription_models import TranscribedChunk
from src.core.interface.transcriber_interface import TranscriberInterface


class FasterWhisperTranscriber(TranscriberInterface):
    """
    Transcriber class for faster-Whisper.
    """

    def __init__(self, model_name: str, **kwargs):
        """
        Initializes the faster-whisper locally with the given model name, .
        """
        self.client = WhisperModel(model_name, device="cpu", **kwargs)

    def transcribe_segments_timestamp(
        self, audio_path: Union[BinaryIO, str], **kwargs
    ) -> List[TranscribedChunk]:
        """
        Transcribe the given audio file using Whisper Fireworks with segment-level timestamps and return the transcription.
        Args:
            - audio_path: path of audio file.
            - **kwargs: Additional arguments for the transcription model.
        Return:
            - Transcription of the audio file.
        """
        try:
            segments, info = self.client.transcribe(
                audio=audio_path,
                word_timestamps=False,
                **kwargs,
            )
            print("********************")
            segments = [
                TranscribedChunk(
                    text=segment.text,
                    start=segment.start,
                    end=segment.end,
                )
                for segment in segments
            ]
            return segments
        except Exception as e:
            raise Exception(f"Error during transcription: {str(e)}")

    def transcribe_words_timestamp(
        self, audio_path: Union[BinaryIO, str], **kwargs
    ) -> List[TranscribedChunk]:
        """
        Transcribe the given audio file using Whisper Fireworks with word-level timestamps and return the transcription.
        Args:
            - audio_path: path of audio file.
            - **kwargs: Additional arguments for the transcription model.
        Return:
            - Transcription of the audio file.
        """
        try:
            segments, info = self.client.transcribe(
                audio=audio_path,
                word_timestamps=True,
                **kwargs,
            )
            segments = [
                TranscribedChunk(
                    text=segment.text,
                    start=segment.start,
                    end=segment.end,
                )
                for segment in segments
            ]
            return segments
        except Exception as e:
            raise Exception(f"Error during transcription: {str(e)}")
