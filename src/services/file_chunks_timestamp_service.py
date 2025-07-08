from typing import BinaryIO, List, Union

from src.core import TranscriberInterface, AlignerInterface
from src.models import ParagraphAlignment


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
        paragraphs: List[str],
        audio: Union[BinaryIO, str],
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
            print(f"start pipeline..")
            if not paragraphs or not audio:
                return []

            transcribed_segments_with_words = (
                self.transcriber.transcribe_segments_with_words_timestamp(
                    audio_path=audio,
                )
            )

            if not transcribed_segments_with_words:
                return []
            print("transcription completed.")
            paragraphs_timestamps = []
            for paragraph in paragraphs:
                # Align the paragraph with audio segments timestamp
                segment_alignment = self.aligner.align_paragraph_with_segments(
                    paragraph, transcribed_segments_with_words.segments
                )
                print(f"segment alignment: {segment_alignment}")
                # Align the paragraph with audio words timestamp
                if segment_alignment:
                    # Get the start word of the paragraph
                    start_segment_words = [
                        word
                        for word in transcribed_segments_with_words.words
                        if str(word.segment_id)
                        == str(segment_alignment.best_start_match.id)
                    ]
                    print(
                        f"length of start_segment_words: {len(start_segment_words)}: {start_segment_words}"
                    )
                    paragraph_start_word = self.aligner.align_paragraph_with_words(
                        paragraph=paragraph,
                        words=start_segment_words,
                    )
                    print(f"paragraph_start_word: {type(paragraph_start_word)}: {paragraph_start_word}")
                    paragraph_start = (
                        paragraph_start_word
                        if paragraph_start_word.best_start_match and paragraph_start_word.best_start_match.score > 0.5
                        else segment_alignment
                    )
                    # Get the end word of the paragraph
                    end_segments_words = [
                        word
                        for word in transcribed_segments_with_words.words
                        if str(word.segment_id)
                        == str(segment_alignment.best_end_match.id)
                    ]
                    paragraph_end_word = self.aligner.align_paragraph_with_words(
                        paragraph=paragraph, words=end_segments_words
                    )
                    print(f"paragraph_end_word: {type(paragraph_end_word)}: {paragraph_end_word}")
                    paragraph_end = (
                        paragraph_end_word
                        if paragraph_end_word.best_end_match and paragraph_end_word.best_end_match.score > 0.5
                        else segment_alignment
                    )
                    # Create a ParagraphAlignment object with the paragraph and its timestamps
                    paragraphs_timestamps.append(
                        ParagraphAlignment(
                            paragraph=paragraph,
                            start=paragraph_start.start,
                            end=paragraph_end.end,
                            best_start_match=paragraph_start.best_start_match,
                            best_end_match=paragraph_end.best_end_match,
                        )
                    )

                else:
                    raise Exception(f"No alignment found for paragraph: {paragraph}")
            return paragraphs_timestamps
        except Exception as e:
            raise Exception(f"Error in get_paragraphs_timestamp: {str(e)}")
