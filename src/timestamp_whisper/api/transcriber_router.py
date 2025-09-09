import io
from typing import Literal, Optional
from fastapi import APIRouter, File, Query, UploadFile, HTTPException
from pydantic import Field

from timestamp_whisper.core.types import FasterWhisperModel, TranscriberType
from timestamp_whisper.core.factory.transcriber_factory import TranscriberFactory
from timestamp_whisper.models.transcription_models import SegmentTranscriptionModelWithWords
from timestamp_whisper.services import TranscriberService
from timestamp_whisper.utils import convert_video_to_audio, detect_file_type


transcriber_router = APIRouter()


# Helper functions
# Get the pipeline for the given transcriber and aligner types
def get_pipeline(
    transcriber_type: Optional[str] = TranscriberType.MODAL_WHISPER,
    transcribe_model: Optional[str] = FasterWhisperModel.LARGE_V3,
):
    try:
        transcriber = TranscriberFactory.get_transcriber(
            transcriber_type=transcriber_type,
            model_name=transcribe_model,
        )

        pipeline = TranscriberService(
            transcriber=transcriber,
        )
        return pipeline
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Endpoints

# transcriber_router.post("/
@transcriber_router.post("/words", response_model=SegmentTranscriptionModelWithWords)
async def transcribe_with_words_timestamp(
    media_file: UploadFile = File(...),
    transcriber_backend: Literal["local", "modal"] = Query(
        default="modal", description="Backend to run transcriber"
    ),
):
    try:
        media_file_bytes = await media_file.read()
        if not media_file_bytes:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")

        # Detect MIME type
        mimetypes = detect_file_type(file_bytes=media_file_bytes)
        if not mimetypes.startswith("video/") and not mimetypes.startswith("audio/"):
            raise HTTPException(
                status_code=400,
                detail="Invalid file format. Please upload a video or audio file.",
            )
        elif mimetypes.startswith("video/"):
            binary_audio = await convert_video_to_audio(
                video_bytes=media_file_bytes, video_name=media_file.filename
            )
        else:
            binary_audio = io.BytesIO(media_file_bytes)

        # Create pipeline
        transcriber_type = (
            TranscriberType.MODAL_WHISPER
            if transcriber_backend == "modal"
            else TranscriberType.FASTER_WHISPER
        )
        pipeline = get_pipeline(transcriber_type=transcriber_type)

        # Align paragraphs with audio
        result = pipeline.get_paragraphs_timestamp(
             audio=binary_audio
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the request: {str(e)}",
        )