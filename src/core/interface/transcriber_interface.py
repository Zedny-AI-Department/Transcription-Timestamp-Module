from abc import ABC, abstractmethod
from typing import List

from src.models import TranscribedChunk


class TranscriberInterface(ABC):
    """
    Abstract base class for transcribers.
    """

    @abstractmethod
    def transcribe_segments_timestamp(
        self, audio: bytes, model_name: str, **args
    ) -> List[TranscribedChunk]:
        """
        Transcribe the given audio file with segments timestamp and return the transcription.
        Args:
            - audio: Bytes of the audio to transcribe.
            - model_name: Name of the model to use for transcription.
            - **args: Additional arguments for the transcription model.
        Return:
            - Transcription of the audio file.
        """
        raise NotImplementedError

    @abstractmethod
    def transcribe_words_timestamp(
        self, audio_file: bytes, model_name: str, **args
    ) -> List[TranscribedChunk]:
        """
        Transcribe the given audio file with words timestamp and return the transcription.
        Args:
            - audio_file: Bytes of the audio to transcribe.
            - model_name: Name of the model to use for transcription.
            - **args: Additional arguments for the transcription model.
        Return:
            - Transcription of the audio file.
        """
        raise NotImplementedError
