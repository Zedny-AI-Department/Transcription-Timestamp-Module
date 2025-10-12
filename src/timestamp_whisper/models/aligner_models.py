from typing import List
from pydantic import BaseModel, Field

from timestamp_whisper.models import TranscribedChunk
from timestamp_whisper.models.transcription_models import WordTranscriptionModel


class MatchChunk(TranscribedChunk):
    """
    Model representing a matcher chunk with additional score attribute.
    """

    score: float = Field(
        description="Score of the match, indicating the similarity between the segment and the search sentence."
    )


class ParagraphAlignment(BaseModel):
    """
    Model representing the alignment of a paragraph with its start and end timestamps.
    """

    paragraph: str = Field(
        ..., description="The paragraph text that is aligned with audio segments."
    )
    start: float = Field(..., description="Start time of the paragraph in seconds.")
    end: float = Field(..., description="End time of the paragraph in seconds.")
    best_start_match: MatchChunk = Field(
        ..., description="The best matching segment for the paragraph."
    )
    best_end_match: MatchChunk = Field(
        ..., description="The best matching segment for the paragraph."
    )


class ParagraphAlignmentWithWords(ParagraphAlignment):
    """
    Model representing the alignment of a paragraph with its start and end timestamps and words.
    """
    paragraph_words: List[WordTranscriptionModel] = Field(
        ..., description="Words in the paragraph."
    )
    paragraph_index: int = Field(
        ..., description="Index of the paragraph."
    )


class ParagraphItem(BaseModel):
    text: str = Field(
        description="Paragraph text."
    )
    paragraph_index: int