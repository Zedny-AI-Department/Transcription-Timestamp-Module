from abc import ABC, abstractmethod
from typing import List

from src.models import TranscribedChunk
from src.models.aligner_models import ParagraphAlignment


class AlignerInterface(ABC):
    """
    Abstract base class for aligners.
    """

    @abstractmethod
    def align_paragraph_with_chunks(
        self, paragraph: str, chunks: List[TranscribedChunk], search_length: int = 10,  **kwargs
    ) -> ParagraphAlignment:
        """
        Align the given paragraph with audio segments timestamp.
        Args:
            - paragraph: The paragraph to align with audio segments.
            - chunks: List of audio segments with their timestamps.
            - **kwargs: Additional arguments for alignment.
            - search_length: Number of words to consider for fuzzy matching (default is 10).
        Return:
            - Start and End time of paragraph.
        """
        raise NotImplementedError
