from typing import List
from Levenshtein import ratio

from src.core.types import DEFAULT_SEARCH_SEGMENT_SIZE
from src.core import AlignerInterface
from src.models import MatchChunk
from src.models import TranscribedChunk, SegmentTranscriptionModel, WordTranscriptionModel
from src.models import ParagraphAlignment


class FuzzyAligner(AlignerInterface):
    """
    Fuzzy Aligner class for aligning audio transcriptions with timestamps.
    This class implements the AlignerInterface and provides methods to align paragraphs with audio segments.
    """

    def __init__(self):
        """
        Initializes the FuzzyAligner with.
        """
        pass

    def align_paragraph_with_segments(
        self, paragraph: str, segments: List[SegmentTranscriptionModel]
    ) -> ParagraphAlignment:
        """
        Align the given paragraph with audio segments timestamp.
        Args:
            - paragraph: The paragraph to align with audio segments.
            - segments: List of audio segments with their timestamps.
            - search_length: Number of words to consider for fuzzy matching (default is 10).
        Return:
            - Start and End time of paragraph.
        """
        # Validate inputs
        if not segments:
            return None
        if not paragraph or paragraph.strip() == "":
            return None

        # Find the most similar segment to the paragraph start with fuzzy matching
        paragraph_start = " ".join(paragraph.strip().split(" ")[:DEFAULT_SEARCH_SEGMENT_SIZE] if paragraph.strip() else "")
        start_match: MatchChunk = self._get_similar_segment(paragraph_start, segments)

        # Find the most similar segment to the paragraph end with fuzzy matching
        paragraph_end = " ".join(paragraph.strip().split(" ")[-DEFAULT_SEARCH_SEGMENT_SIZE:] if paragraph.strip() else "")
        end_match: MatchChunk = self._get_similar_segment(paragraph_end, segments)

        # Return the alignment with start and end times
        return ParagraphAlignment(
            paragraph=paragraph, 
            start=start_match.start if start_match else 0, 
            end=end_match.end if end_match else 0,
            best_start_match=start_match,
            best_end_match=end_match
        )

    def align_paragraph_with_words(
        self, paragraph: str, words: List[WordTranscriptionModel]
    ) -> ParagraphAlignment:
        """
        Align the given paragraph with audio segments timestamp.
        Args:
            - paragraph: The paragraph to align with audio segments.
            - words: List of audio segments with their timestamps.
            - search_length: Number of words to consider for fuzzy matching (default is 10).
        Return:
            - Start and End time of paragraph.
        """
        # Validate inputs
        if not words:
            return None
        if not paragraph or paragraph.strip() == "":
            return None

        # Find the most similar segment to the paragraph start with fuzzy matching
        paragraph_start = paragraph.strip().split(" ")[0] if paragraph.strip() else ""
        start_match: MatchChunk = self._get_similar_segment(paragraph_start, words)

        # Find the most similar segment to the paragraph end with fuzzy matching
        paragraph_end = paragraph.strip().split(" ")[-1] if paragraph.strip() else ""
        end_match: MatchChunk = self._get_similar_segment(paragraph_end, words)

        # Return the alignment with start and end times
        return ParagraphAlignment(
            paragraph=paragraph, 
            start=start_match.start if start_match else 0, 
            end=end_match.end if end_match else 0,
            best_start_match=start_match,
            best_end_match=end_match
        )

    def _get_similar_segment(self,
        search_sentence: str, chunks: List[TranscribedChunk]
    ) -> MatchChunk:
        """
        Find the most similar segment to the search sentence using fuzzy matching.
        Args:
            - search_sentence: The sentence to search for in the segments.
            - chunks: List of audio segments to search within.
        Return:
            - MatchChunk containing the most similar segment's text, start time, end time, and score.
        """
        # Validate inputs
        if not chunks:
            return None
        if not search_sentence or search_sentence.strip() == "":
            return None

        # Get the segment with the highest similarity score
        max_score = 0
        best_match = None
        for segment in chunks:
            if segment and segment.text.strip() != "":
                score = ratio(segment.text, search_sentence)
                if max_score ==0 or score > max_score:
                    max_score = score
                    best_match = segment

        return (
            MatchChunk(
                id=best_match.id,
                text=best_match.text,
                start=best_match.start,
                end=best_match.end,
                score=max_score,
            )
        )
