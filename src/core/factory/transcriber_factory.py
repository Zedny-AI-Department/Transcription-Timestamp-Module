import os
from dotenv import load_dotenv

from src.core import TranscriberInterface
from src.core.types import TranscriberType
from src.core.transcriber import WhisperFireworksTranscriber

# Load environment variables from .env file
load_dotenv()


class TranscriberFactory:
    """
    Factory class to create transcription instances based on the model name.
    """

    @staticmethod
    def get_transcriber(transcriber_type: str, **kwargs) -> TranscriberInterface:
        """
        Get the appropriate transcriber instance based on the model name.
        Args:
            - transcriber_type: Type of the transcriber (e.g., "whisper_fireworks", "elevenlabs").
            - model_name: Name of the transcription model.
            - **kwargs: Additional arguments for the transcriber.
        Returns:
            - An instance of the transcriber.
        """
        if transcriber_type == TranscriberType.WHISPER_FIREWORKS:
            return WhisperFireworksTranscriber(
                api_key= "fw_3ZSi76TGkzXALg8KWc4kyzak" #os.getenv("FIREWORKS_API"), **kwargs
            )

        raise ValueError(
            f"Transcriber type must be one of: {[t.value for t in TranscriberType]} but got {transcriber_type}"
        )
