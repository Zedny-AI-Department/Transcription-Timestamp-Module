from abc import ABC, abstractmethod
from typing import List

from src.models import TranscribedChunk
from src.models.aligner_models import ParagraphAlignment


class AlignerInterface(ABC):
    """
    Abstract base class for aligners.
    """

    @abstractmethod
    def align_paragraph_timestamp_with_segments(
        self, paragraph: str, segments: List[TranscribedChunk], **kwargs
    ) -> ParagraphAlignment:
        """
        Align the given paragraph with audio segments timestamp.
        Args:
            - paragraph: The paragraph to align with audio segments.
            - segments: List of audio segments with their timestamps.
            - **kwargs: Additional arguments for alignment.
        Return:
            - Start and End time of paragraph.
        """
        raise NotImplementedError
