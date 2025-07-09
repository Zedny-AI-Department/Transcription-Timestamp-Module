from typing import BinaryIO, List, Union
import uuid
from faster_whisper import WhisperModel

from src.models import SegmentTranscriptionModel, SegmentTranscriptionModelWithWords, WordTranscriptionModel
from src.core.interface.transcriber_interface import TranscriberInterface


class FasterWhisperTranscriber(TranscriberInterface):
    """
    Transcriber class for faster-Whisper.
    """

    def __init__(self, model_name: str, **kwargs):
        """
        Initializes the faster-whisper locally with the given model name, .
        """
        self.client = WhisperModel(model_name, device="cpu", **kwargs)

    def transcribe_segments_timestamp(
        self, audio_path: Union[BinaryIO, str], **kwargs
    ) -> List[SegmentTranscriptionModel]:
        """
        Transcribe the given audio file using Whisper Fireworks with segment-level timestamps and return the transcription.
        Args:
            - audio_path: path of audio file.
            - **kwargs: Additional arguments for the transcription model.
        Return:
            - Transcription of the audio file.
        """
        try:
            segments, info = self.client.transcribe(
                audio=audio_path,
                word_timestamps=False,
                **kwargs,
            )
            segments = [
                SegmentTranscriptionModel(
                    segment_id=str(segment.id),
                    text=segment.text.strip(),
                    start=segment.start,
                    end=segment.end,
                )
                for segment in segments
            ]
            return segments
        except Exception as e:
            raise Exception(f"Error during transcription: {str(e)}")

    def transcribe_segments_with_words_timestamp(
        self, audio_path: Union[BinaryIO, str], **kwargs
    ) -> SegmentTranscriptionModelWithWords:
        """
        Transcribe the given audio file using Whisper with segment-level and  word-level timestamps and return the transcription.
        Args:
            - audio_path: path of audio file.
            - **kwargs: Additional arguments for the transcription model.
        Return:
            - Transcription of the audio file.
        """
        try:
            segments, info = self.client.transcribe(
                audio=audio_path,
                word_timestamps=True,
                **kwargs,
            )
            print("start transcription..")
            segments_timestamps = []
            words_timestamps = []
            for segment in segments:
                print(f"{segment.id}: {segment.text}, {segment.start}, {segment.end}")
                print("------------")
                segments_timestamps.append(
                    SegmentTranscriptionModel(
                        id=str(segment.id),
                        text=segment.text.strip(),
                        start=segment.start,
                        end=segment.end,
                    )
                )
                for word in segment.words:
                    words_timestamps.append(
                        WordTranscriptionModel(
                            id=str(uuid.uuid4()),
                            segment_id=str(segment.id),
                            text=word.word,
                            start=word.start,
                            end=word.end,
                        )
                    )

            return SegmentTranscriptionModelWithWords(
                segments=segments_timestamps,
                words=words_timestamps,
)
        except Exception as e:
            raise Exception(f"Error during transcription: {str(e)}")
