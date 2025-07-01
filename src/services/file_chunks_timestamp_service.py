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
            print(
                f"Processing {len(paragraphs)} paragraphs"
            )
            if not paragraphs or not audio:
                return []

            transcribed_segments = self.transcriber.transcribe_segments_timestamp(
                audio_path=audio
            )

            print(
                f"Transcribed {len(transcribed_segments)} segments"
            )
            if not transcribed_segments:
                return []

            # transcribed_words = self.transcriber.transcribe_words_timestamp(
            #     audio_path=audio
            # )

            # print(
            #     f"Transcribed {len(transcribed_words)} segments "
            # )

            paragraphs_timestamps = []
            for paragraph in paragraphs:
                alignment = self.aligner.align_paragraph_timestamp_with_segments(
                    paragraph, transcribed_segments
                )
                print(f"Aligned paragraph : {alignment}")
                paragraphs_timestamps.append(alignment)
                print(f"len: {len(paragraphs_timestamps)}")
            return paragraphs_timestamps
        except Exception as e:
            raise Exception(f"Error in get_paragraphs_timestamp: {str(e)}")
