from typing import List

from src.core import TranscriberInterface, AlignerInterface
from src.models import ParagraphAlignment


class FileChunksTimestampPipeline:
    """
    Pipeline for processing file chunks with timestamps.

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
        self, paragraphs: List[str], audio: bytes, transcriber_model: str = "whisper-v3"
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
                f"Processing {len(paragraphs)} paragraphs with audio of size bytes using model {transcriber_model}"
            )
            if not paragraphs or not audio:
                return []

            transcribed_chunks = self.transcriber.transcribe_segments_timestamp(
                audio=audio, model_name=transcriber_model
            )
            print(
                f"Transcribed {len(transcribed_chunks)} segments from audio with model {transcriber_model}"
            )
            if not transcribed_chunks:
                return []
            paragraphs_timestamps = []
            for paragraph in paragraphs:
                alignment = self.aligner.align_paragraph_timestamp_with_segments(
                    paragraph, transcribed_chunks
                )
                print(
                    f"Aligned paragraph : {alignment}"
                )
                paragraphs_timestamps.append(alignment)
                print(f"len: {len(paragraphs_timestamps)}")
            return paragraphs_timestamps
        except Exception as e:            
            raise Exception(f"Error in get_paragraphs_timestamp: {str(e)}")
