import io
import modal

from timestamp_whisper.config.modal_app import faster_whisper_image, app
from timestamp_whisper.utils.video_compression_util import decompress_bytes


@app.cls(
    image=faster_whisper_image,
    gpu="T4",
    timeout=1000,
)
class ModalWhisperTranscriber:
    """
    ModalWhisperTranscriber is a class for transcribing audio using the faster-whisper model within a Modal environment.
    Methods:
        enter(self):
            Initializes the WhisperModel with the specified configuration when entering the Modal container.
        transcribe(self, audio_bytes: bytes, **kwargs):
            Transcribes the provided audio bytes using the loaded WhisperModel.
    """

    @modal.enter()
    def enter(self):
        from faster_whisper import WhisperModel
        self.model = WhisperModel("large-v3")  # compute_type="float32", device="cuda"

    @modal.method(is_generator=True)
    def transcribe(self, audio_bytes: bytes, **kwargs):
        """
        Transcribes the given audio bytes using the loaded model.
        Args:
            audio_bytes (bytes): The audio data in bytes format to be transcribed.
            **kwargs: Additional keyword arguments to pass to the model's transcribe method.
        Returns:
            segments: The transcription segments returned by the model.
        Raises:
            ValueError: If the provided audio file is empty.
        """
        # Convert bytes back to BytesIO for faster-whisper
        decompressed_audio_bytes = decompress_bytes(audio_bytes)
        audio_file = io.BytesIO(decompressed_audio_bytes)
        if not audio_file:
            raise ValueError("Audio file is empty")
        segments, info = self.model.transcribe(audio_file, **kwargs)
        return segments
