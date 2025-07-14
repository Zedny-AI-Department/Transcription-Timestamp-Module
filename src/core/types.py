from enum import Enum


class TranscriberType(str, Enum):
    """
    Enum-like class for different transcription types.
    """

    FASTER_WHISPER = "faster_whisper"
    MODAL_WHISPER = "modal_whisper"


class AlignerType(str, Enum):
    """
    Enum-like class for different transcription types.
    """

    FUZZY_ALIGNER = "fuzzy_aligner"
    FUZZYWUZZY_ALIGNER = "fuzzywuzzy_aligner"


class FasterWhisperModel(str, Enum):
    """
    Enum-like class for different Faster Whisper models.
    """

    LARGE_V3 = "large-v3"
    MEDIUM = "medium"
    SMALL = "small"
    TINY = "tiny"
    BASE = "base"


# Defaults

DEFAULT_SEARCH_SEGMENT_SIZE: int = 8
