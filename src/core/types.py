from enum import Enum


class TranscriberType(str, Enum):
    """
    Enum-like class for different transcription types.
    """

    WHISPER_FIREWORKS = "whisper_fireworks"


class AlignerType(str, Enum):
    """
    Enum-like class for different transcription types.
    """

    FUZZY_ALIGNER = "fuzzy_aligner"
