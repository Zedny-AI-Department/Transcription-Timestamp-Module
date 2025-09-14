from typing import BinaryIO, List, Union

from timestamp_whisper.core import TranscriberInterface, AlignerInterface
from timestamp_whisper.models import ParagraphAlignment
from timestamp_whisper.models.aligner_models import ParagraphAlignmentWithWords, ParagraphItem


class FileChunksTimestampService:
    """
    Service for processing file chunks with timestamps.

    This class is used to create a pipeline that processes file chunks
    and returns their timestamps using a specified transcriber and aligner.
    """

    def __init__(self, transcriber: TranscriberInterface, aligner: AlignerInterface):
        """
        Initializes the FileChunksTimestampPipeline with a transcriber and aligner.
        """
        self.transcriber = transcriber
        self.aligner = aligner

    def get_paragraphs_timestamp(
        self,
        paragraphs: List[ParagraphItem],
        audio: BinaryIO,
    ) -> List[ParagraphAlignment]:
        """
        Get timestamps for paragraphs aligned with audio segments.
        Args:
            - paragraphs: List of paragraphs to be aligned with audio segments.
            - audio: Audio data to be processed.
            - transcriber_model: Name of the transcription model to use.
        Returns:
            - List of ParagraphAlignment objects containing the start timestamps of each paragraph.
        """
        try:
            if not paragraphs or not audio:
                return []

            transcribed_segments_with_words = (
                self.transcriber.transcribe_segments_with_words_timestamp(
                    audio_path=audio,
                    vad_filter=True,
                    vad_parameters=dict(
                        threshold=0.3,
                        min_speech_duration_ms=1000
                    ),
                    chunk_length=3,
                )
            )
            if not transcribed_segments_with_words:
                return []
            paragraphs_timestamps = []
            for paragraph in paragraphs:
                # Align the paragraph with audio segments timestamp
                segment_alignment = self.aligner.align_paragraph_with_segments(
                    paragraph.text, transcribed_segments_with_words.segments, search_length=10
                )
                # Align the paragraph with audio words timestamp
                if segment_alignment:
                    # Get the start word of the paragraph
                    start_segments_words = [
                        word
                        for word in transcribed_segments_with_words.words
                        if str(word.segment_id)
                        in [str(segment_alignment.best_start_match.id), str(int(segment_alignment.best_start_match.id) - 1), str(int(segment_alignment.best_start_match.id) - 2)]
                    ]
                    paragraph_start_word = self.aligner.align_paragraph_with_words(
                        paragraph=paragraph.text,
                        words=start_segments_words,
                    )
                    paragraph_start = (
                        paragraph_start_word
                        if paragraph_start_word.best_start_match
                        and paragraph_start_word.best_start_match.score > 0.5
                        else segment_alignment
                    )

                    # Get the start word of the paragraph
                    end_segments_words = [
                        word
                        for word in transcribed_segments_with_words.words
                        if str(word.segment_id)
                        in [str(segment_alignment.best_end_match.id), str(int(segment_alignment.best_end_match.id) +  1), str(int(segment_alignment.best_end_match.id) +  2)]
                    ]
                    paragraph_end_word = self.aligner.align_paragraph_with_words(
                        paragraph=paragraph.text, words=end_segments_words
                    )
                    paragraph_end = (
                        paragraph_end_word
                        if paragraph_end_word.best_end_match
                        and paragraph_end_word.best_end_match.score > 0.5
                        else segment_alignment
                    )
                    # Get paragraph words
                    paragraph_words = [word for word in transcribed_segments_with_words.words if word.start >=
                                       paragraph_start.start and word.end <= paragraph_end.end]
                    # Create a ParagraphAlignment object with the paragraph and its timestamps
                    paragraphs_timestamps.append(
                        ParagraphAlignmentWithWords(
                            paragraph=paragraph.text,
                            paragraph_index=paragraph.paragraph_index,
                            start=paragraph_start.start,
                            end=paragraph_end.end,
                            best_start_match=paragraph_start.best_start_match,
                            best_end_match=paragraph_end.best_end_match,
                            paragraph_words=paragraph_words,
                        )
                    )

                else:
                    raise Exception(f"No alignment found for paragraph: {paragraph}")
            return paragraphs_timestamps
        except Exception as e:
            raise Exception(f"Error in get_paragraphs_timestamp: {str(e)}")
