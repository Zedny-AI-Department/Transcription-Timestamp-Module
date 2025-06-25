from typing import List
from fireworks.client.audio import AudioInference

from src.core import TranscriberInterface
from src.models import TranscribedChunk


class WhisperFireworksTranscriber(TranscriberInterface):
    """
    Transcriber class for Whisper Fireworks.
    """

    def __init__(self, api_key: str, **kwargs):
        """
        Initializes the FireworksClient with the given model name, model base URL, and API key.
        """
        self.client = AudioInference(
            api_key=api_key,
            base_url="https://audio-prod.us-virginia-1.direct.fireworks.ai",
            **kwargs,
        )

    def transcribe_segments_timestamp(
        self, audio: bytes, model_name: str, **kwargs
    ) -> List[TranscribedChunk]:
        """
        Transcribe the given audio file using Whisper Fireworks with segment-level timestamps and return the transcription.
        Args:
            - audio: Bytes of the audio to transcribe.
            - model_name: Name of the model to use for transcription.
            - **kwargs: Additional arguments for the transcription model.
        Return:
            - Transcription of the audio file.
        """
        try:
            result = self.client.transcribe(
                audio=audio,
                model=model_name,
                response_format="verbose_json",
                timestamp_granularities=["segment"],
                **kwargs,
            )
            segments = [
                TranscribedChunk(
                    text=segment.text,
                    start=segment.start,
                    end=segment.end,
                )
                for segment in result.segments
            ]
            return segments
        except Exception as e:
            raise Exception(f"Error during transcription: {str(e)}")

    def transcribe_words_timestamp(
        self, audio: bytes, model_name: str, **kwargs
    ) -> List[TranscribedChunk]:
        """
        Transcribe the given audio file using Whisper Fireworks with word-level timestamps and return the transcription.
        Args:
            - audio: Bytes of the audio to transcribe.
            - model_name: Name of the model to use for transcription.
            - **kwargs: Additional arguments for the transcription model.
        Return:
            - Transcription of the audio file.
        """
        try:
            result = self.client.transcribe(
                audio=audio,
                model=model_name,
                response_format="verbose_json",
                timestamp_granularities=["word"],
                **kwargs,
            )
            segments = [
                TranscribedChunk(
                    text=word["text"],
                    start=word["start"],
                    end=word["end"],
                )
                for word in result.words
            ]
            return segments
        except Exception as e:
            raise Exception(f"Error during transcription: {str(e)}")
