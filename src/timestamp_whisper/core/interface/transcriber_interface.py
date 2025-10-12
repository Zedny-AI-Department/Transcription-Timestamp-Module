from abc import ABC, abstractmethod
from typing import BinaryIO, List, Union

from timestamp_whisper.models import SegmentTranscriptionModel, SegmentTranscriptionModelWithWords


class TranscriberInterface(ABC):
    """
    Abstract base class for transcribers.
    """

    @abstractmethod
    def transcribe_segments_timestamp(
        self, audio_path: Union[BinaryIO, str], **kwargs
    ) -> List[SegmentTranscriptionModel]:
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
    def transcribe_segments_with_words_timestamp(
        self, audio_path: Union[BinaryIO, str], **kwargs
    ) -> SegmentTranscriptionModelWithWords:
        """
        Transcribe the given audio file using Whisper Fireworks with segment-level timestamps and return the transcription.
        Args:
            - audio_path: path of audio file.
            - **args: Additional arguments for the transcription model.
        Return:
            - Transcription of the audio file.
        """
        raise NotImplementedError
