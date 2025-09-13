import string
from typing import List
from fuzzywuzzy import fuzz

from timestamp_whisper.core import AlignerInterface
from timestamp_whisper.models import MatchChunk
from timestamp_whisper.models import SegmentTranscriptionModel, WordTranscriptionModel
from timestamp_whisper.models import ParagraphAlignment
from timestamp_whisper.core.types import DEFAULT_SEARCH_SEGMENT_SIZE


class FuzzyWuzzyAligner(AlignerInterface):
    """
    FuzzyWuzzy Aligner class for aligning audio transcriptions with timestamps.
    This class implements the AlignerInterface and provides methods to align paragraphs with audio segments.
    """

    def __init__(self):
        """
        Initializes the FuzzyAligner with.
        """
        pass

    def align_paragraph_with_segments(
        self, paragraph: str, segments: List[SegmentTranscriptionModel],
        search_length: int = DEFAULT_SEARCH_SEGMENT_SIZE
    ) -> ParagraphAlignment:
        """
        Align the given paragraph with audio segments timestamp.
        Args:
            - paragraph: The paragraph to align with audio segments.
            - segments: List of audio segments with their timestamps.
            - search_length: Number of words to consider for fuzzy matching (default is 8).
        Return:
            - Start and End time of paragraph.
        """
        # Validate inputs
        if not segments:
            return None
        if not paragraph or paragraph.strip() == "":
            return None

        # Find the most similar segment to the paragraph start with fuzzy matching
        paragraph_start = " ".join(paragraph.strip().split(" ")[:search_length] if paragraph.strip() else "")
        start_match: MatchChunk = self._get_similar_segment(paragraph_start, segments)

        # Find the most similar segment to the paragraph end with fuzzy matching
        paragraph_end = " ".join(paragraph.strip().split(
            " ")[-search_length:] if paragraph.strip() else "")
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
        paragraph_start =  " ".join(paragraph.strip().split(" ")[0:3]) if paragraph.strip() else ""
        start_match: MatchChunk = self._get_similar_word(paragraph_start, words)
        # Find the most similar segment to the paragraph end with fuzzy matching
        paragraph_end = " ".join(paragraph.strip().split(" ")[-3:]) if paragraph.strip() else ""
        end_match: MatchChunk = self._get_similar_word(paragraph_end, words)
        # Return the alignment with start and end times
        return ParagraphAlignment(
            paragraph=paragraph, 
            start=start_match.start if start_match else 0, 
            end=end_match.end if end_match else 0,
            best_start_match=start_match,
            best_end_match=end_match
        )

    def _get_similar_segment(self,
        search_sentence: str, segments: List[SegmentTranscriptionModel]
    ) -> MatchChunk:
        """
        Find the most similar segment to the search sentence using fuzzy matching.
        Args:
            - search_sentence: The sentence to search for in the segments.
            - segments: List of audio segments to search within.
        Return:
            - MatchChunk containing the most similar segment's text, start time, end time, and score.
        """
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
                ratio_score = fuzz.ratio(self._clean_text(segment.text).lower().strip(), self._clean_text(search_sentence).lower().strip())  
                partial_score = fuzz.partial_ratio(
                    self._clean_text(segment.text).lower().strip(), self._clean_text(search_sentence).lower().strip())
                token_set_score = fuzz.token_set_ratio(self._clean_text(segment.text).lower().strip(), self._clean_text(search_sentence).lower().strip())
                composite_score = (partial_score * 0.5 + 
                  ratio_score * 0.3 + 
                  token_set_score * 0.2)

                if max_score == 0 or composite_score > max_score:
                    max_score = composite_score
                    best_match = segment

        return (
            MatchChunk(
                id=best_match.id,
                text=best_match.text,
                start=best_match.start,
                end=best_match.end,
                score=max_score / 100,
            )
        )

    def _get_similar_word(self,
        search_sentence: str, words: List[WordTranscriptionModel]
    ) -> MatchChunk:
        """
        Find the most similar segment to the search sentence using fuzzy matching.
        Args:
            - search_sentence: The sentence to search for in the segments.
            - words: List of audio segments to search within.
        Return:
            - MatchChunk containing the most similar segment's text, start time, end time, and score.
        """
        # Validate inputs
        if not words:
            return None
        if not search_sentence or search_sentence.strip() == "":
            return None

        # Create 2-word sequences from the word list
        word_sequences = []
        for i in range(len(words) - 2):  # -1 because we need pairs
            word1 = words[i]
            word2 = words[i + 1]
            word3 = words[i + 2]

            # Skip if either word is invalid
            if not word1 or not word2 or not word1.text.strip() or not word2.text.strip() or not word3.text.strip():
                continue

            # Create combined text and timing for the 2-word sequence
            combined_text = f"{word1.text.strip()} {word2.text.strip()} {word3.text.strip()}"
            start_time = word1.start
            end_time = word3.end

            # Create a sequence object with combined properties
            sequence = {
                'text': combined_text,
                'start': start_time,
                'end': end_time,
                'id': f"{word1.id}-{word2.id}--{word3.id}"  # Combined ID
            }
            word_sequences.append(sequence)

        # If no valid sequences found, return None
        if not word_sequences:
            return None

        # Get the segment with the highest similarity score
        max_score = 0
        best_match = None
        for sequence in word_sequences:
            score = fuzz.ratio(
                self._clean_text(str(sequence["text"])).lower().strip(), self._clean_text(search_sentence).lower().strip()
            )
            if max_score == 0 or score > max_score:
                max_score = score
                best_match = sequence

        return (
            MatchChunk(
                id=best_match['id'],
                text=best_match['text'],
                start=best_match['start'],
                end=best_match['end'],
                score=max_score / 100,
            )
        )
    
    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean the text by removing punctuation and converting to lowercase."""
        table = str.maketrans("", "", string.punctuation)
        clean_text = text.translate(table)
        return clean_text.lower()
