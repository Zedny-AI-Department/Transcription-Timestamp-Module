import os
from dotenv import load_dotenv

from timestamp_whisper.core import TranscriberInterface
from timestamp_whisper.core.types import TranscriberType
from timestamp_whisper.core.transcriber import FasterWhisperTranscriber, ModalFasterWhisperTranscriber

# Load environment variables from .env file
load_dotenv()


class TranscriberFactory:
    """
    Factory class to create transcription instances based on the model name.
    """

    @staticmethod
    def get_transcriber(
        transcriber_type: str, model_name: str, **kwargs
    ) -> TranscriberInterface:
        """
        Get the appropriate transcriber instance based on the model name.
        Args:
            - transcriber_type: Type of the transcriber (e.g., "FASTER_WHISPER").
            - model_name: Name of the transcription model.
            - **kwargs: Additional arguments for the transcriber.
        Returns:
            - An instance of the transcriber.
        """
        if transcriber_type == TranscriberType.FASTER_WHISPER:
            return FasterWhisperTranscriber(model_name=model_name, **kwargs)
        elif transcriber_type == TranscriberType.MODAL_WHISPER:
            return ModalFasterWhisperTranscriber(model_name=model_name, **kwargs)
        raise ValueError(
            f"Transcriber type must be one of: {[t.value for t in TranscriberType]} but got {transcriber_type}"
        )
