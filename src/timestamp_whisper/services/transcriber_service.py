from typing import BinaryIO, List

from timestamp_whisper.core import TranscriberInterface
from timestamp_whisper.models.transcription_models import SegmentTranscriptionModelWithWords


class TranscriberService:
    """
    Service for transcribe file  with timestamps.
    """

    def __init__(self, transcriber: TranscriberInterface):
        """
        Initializes the TranscriberService with a transcriber and aligner.
        """
        self.transcriber = transcriber

    def get_paragraphs_timestamp(
        self,
        audio: BinaryIO,
    ) -> SegmentTranscriptionModelWithWords:
        """
        Get timestamps for paragraphs aligned with audio segments.
        Args:
            - audio: Audio data to be processed.
        Returns:
            - List of SegmentTranscriptionModelWithWords objects containing the segments with word-level timestamps.
        """
        try:
            transcribed_segments_with_words = (
                self.transcriber.transcribe_segments_with_words_timestamp(
                    audio_path=audio,
                    vad_filter=True,
                    vad_parameters=dict(
                        threshold=0.3,
                    ),
                    chunk_length=3,
                    beam_size=5,  # Use beam search instead of sampling
                    best_of=5,    # Number of candidates when using sampling
                    temperature=0.0,  # Disable sampling randomness
                )
            )

            if not transcribed_segments_with_words:
                return []
            return transcribed_segments_with_words
        except Exception as e:
            raise Exception(f"Error in get_paragraphs_timestamp: {str(e)}")
