from typing import BinaryIO, List, Union
import uuid
import modal

from src.models import (
    SegmentTranscriptionModel,
    SegmentTranscriptionModelWithWords,
    WordTranscriptionModel,
)
from src.core.interface.transcriber_interface import TranscriberInterface


class ModalFasterWhisperTranscriber(TranscriberInterface):
    """
    Transcriber class for faster-Whisper.
    """

    def __init__(self, model_name: str, **kwargs):
        """
        Initializes the faster-whisper locally with the given model name, .
        """
        self.modal_faster_whisper_transcriber_class = modal.Cls.from_name(
            "timestamp_app", "ModalWhisperTranscriber"
        )
        self.model = self.modal_faster_whisper_transcriber_class()

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

            # Read bytes from audio_path
            if isinstance(audio_path, str):
                # It's a file path string
                with open(audio_path, "rb") as f:
                    audio_bytes = f.read()

            else:
                # It's a BinaryIO object (file-like)
                # Go to beginning and read all bytes
                audio_path.seek(0)
                audio_bytes = audio_path.read()
                # Restore original position (optional, depends on your use case)
                audio_path.seek(0)
            segments = self.model.transcribe.remote_gen(
                audio_bytes=audio_bytes,
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
            # Read bytes from audio_path
            if isinstance(audio_path, str):
                # It's a file path string
                with open(audio_path, "rb") as f:
                    audio_bytes = f.read()

            else:
                # It's a BinaryIO object (file-like)
                # Go to beginning and read all bytes
                audio_path.seek(0)
                audio_bytes = audio_path.read()
                # Restore original position (optional, depends on your use case)
                audio_path.seek(0)
            segments = self.model.transcribe.remote_gen(
                audio_bytes=audio_bytes,
                word_timestamps=True,
                **kwargs,
            )
            segments_timestamps = []
            words_timestamps = []
            for segment in segments:
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
