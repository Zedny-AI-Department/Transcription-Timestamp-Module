from typing import List

from timestamp_whisper.core import AlignerInterface
from timestamp_whisper.models import ParagraphAlignment
from timestamp_whisper.models.transcription_models import SegmentTranscriptionModel


class ParagraphAssAlimentService:
    """
    
    """

    def __init__(self, aligner: AlignerInterface):
        """
        Initializes the ParagraphAssAlimentService with an aligner.
        """
        self.aligner = aligner

    def get_paragraphs_timestamp(
        self,
        paragraphs: List[str],
        ass_segments: List[SegmentTranscriptionModel],
    ) -> List[ParagraphAlignment]:
        """
        Get timestamps for paragraphs aligned with ass transcription segments.
        Args:
            - paragraphs: List of paragraphs to be aligned with audio segments.
            - ass_segments (List[SegmentTranscriptionModel]): List of transcription segments to align the paragraphs with.
        Returns:
            - List of ParagraphAlignment objects containing the start timestamps of each paragraph.
        """
        try:
            if not paragraphs or not ass_segments:
                return []

            paragraphs_timestamps = []
            for paragraph in paragraphs:
                # Align the paragraph with audio segments timestamp
                segment_alignment = self.aligner.align_paragraph_with_segments(
                    paragraph, ass_segments,
                    search_length=5
                )
                # Create a ParagraphAlignment object with the paragraph and its timestamps
                paragraphs_timestamps.append(
                    ParagraphAlignment(
                        paragraph=paragraph,
                        start=segment_alignment.start,
                        end=segment_alignment.end,
                        best_start_match=segment_alignment.best_start_match,
                        best_end_match=segment_alignment.best_end_match,
                    )
                )  
            return paragraphs_timestamps
        except Exception as e:
            raise Exception(f"Error while aligning paragraphs with ass file: {str(e)}")
