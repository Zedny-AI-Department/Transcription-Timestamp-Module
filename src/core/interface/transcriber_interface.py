from abc import ABC, abstractmethod
from typing import BinaryIO, List, Union

from src.models import TranscribedChunk


class TranscriberInterface(ABC):
    """
    Abstract base class for transcribers.
    """

    @abstractmethod
    def transcribe_segments_timestamp(
        self, audio_path: Union[BinaryIO, str], **kwargs
    ) -> List[TranscribedChunk]:
        """
        Transcribe the given audio file with segments timestamp and return the transcription.
        Args:
            - audio_path: path of audio file.
            - **args: Additional arguments for the transcription model.
        Return:
            - Transcription of the audio file.
        """
        raise NotImplementedError

    @abstractmethod
    def transcribe_words_timestamp(
        self, audio_path: Union[BinaryIO, str], **kwargs
    ) -> List[TranscribedChunk]:
        """
        Transcribe the given audio file with words timestamp and return the transcription.
        Args:
            - audio_path: path of audio file.
            - **args: Additional arguments for the transcription model.
        Return:
            - Transcription of the audio file.
        """
        raise NotImplementedError
