from pydantic import BaseModel, Field


class TranscribedChunk(BaseModel):
    """
    Model representing a segment of audio with its transcription and timestamps.
    """

    text: str = Field(..., description="Transcription text of the audio segment.")
    start: float = Field(..., description="Start time of the segment in seconds.")
    end: float = Field(..., description="End time of the segment in seconds.")
