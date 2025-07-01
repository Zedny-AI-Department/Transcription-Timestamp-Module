from typing import List
from Levenshtein import ratio

from src.core import AlignerInterface
from src.models import MatchChunk
from src.models import TranscribedChunk
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

    def align_paragraph_timestamp_with_segments(
        self, paragraph: str, segments: List[TranscribedChunk]
    ) -> ParagraphAlignment:
        """
        Align the given paragraph with audio segments timestamp.
        Args:
            - paragraph: The paragraph to align with audio segments.
            - segments: List of audio segments with their timestamps.
        Return:
            - Start and End time of paragraph.
        """
        # Validate inputs
        if not segments:
            return None
        if not paragraph or paragraph.strip() == "":
            return None

        # Find the most similar segment to the paragraph start with fuzzy matching
        paragraph_start = " ".join(paragraph.strip().split(" ")[:10] if paragraph.strip() else "")
        start_match: MatchChunk = self._get_similar_segment(paragraph_start, segments)
        
        print(f"paragraph: {paragraph_start}, best match: {start_match}")
        # Find the most similar segment to the paragraph end with fuzzy matching
        paragraph_end = " ".join(paragraph.strip().split(" ")[-10:] if paragraph.strip() else "")
        end_match: MatchChunk = self._get_similar_segment(paragraph_end, segments)
        print(f"paragraph: {paragraph_end}, best match: {end_match}")
        # Return the alignment with start and end times
        return ParagraphAlignment(
            paragraph=paragraph, start=start_match.start, end=end_match.end
        )

    def _get_similar_segment(self,
        search_sentence: str, segments: List[TranscribedChunk]
    ) -> MatchChunk:
        """
        Find the most similar segment to the search sentence using fuzzy matching.
        Args:
            - search_sentence: The sentence to search for in the segments.
            - segments: List of audio segments to search within.
        Return:
            - MatchChunk containing the most similar segment's text, start time, end time, and score.
        """
        print(f"Searching for similar segment to: {search_sentence}")
        print(f"Number of segments to search in: {len(segments)}")
        # Validate inputs
        if not segments:
            return None
        if not search_sentence or search_sentence.strip() == "":
            return None

        # Get the segment with the highest similarity score
        max_score = 0
        best_match = None
        for segment in segments:
            if segment and segment.text.strip() != "":
                score = ratio(segment.text, search_sentence)
                if score > max_score:
                    max_score = score
                    best_match = segment
        return (
            MatchChunk(
                text=best_match.text,
                start=best_match.start,
                end=best_match.end,
                score=max_score,
            )
            if best_match
            else None
        )
