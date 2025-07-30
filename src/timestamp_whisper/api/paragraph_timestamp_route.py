import io
import json
from typing import List, Literal, Optional
from fastapi import APIRouter, File, Query, UploadFile, HTTPException
from pydantic import BaseModel, Field

from timestamp_whisper.core.types import FasterWhisperModel, TranscriberType, AlignerType
from timestamp_whisper.core.factory.aligner_factory import AlignerFactory
from timestamp_whisper.core.factory.transcriber_factory import TranscriberFactory
from timestamp_whisper.models.aligner_models import ParagraphAlignment
from timestamp_whisper.services import FileChunksTimestampService
from timestamp_whisper.services.align_text_with_transcription import ParagraphAssAlimentService
from timestamp_whisper.utils import convert_video_to_audio, detect_file_type, read_url, read_ass_file


paragraph_timestamp_router = APIRouter()


# Helper functions
# Get the pipeline for the given transcriber and aligner types
def get_pipeline(
    transcriber_type: Optional[str] = TranscriberType.MODAL_WHISPER,
    transcribe_model: Optional[str] = FasterWhisperModel.LARGE_V3,
    aligner_type: Optional[str] = AlignerType.FUZZYWUZZY_ALIGNER,
):
    try:
        transcriber = TranscriberFactory.get_transcriber(
            transcriber_type=transcriber_type,
            model_name=transcribe_model,
        )

        aligner = AlignerFactory.get_aligner(aligner_type=aligner_type)

        pipeline = FileChunksTimestampService(
            transcriber=transcriber,
            aligner=aligner,
        )
        return pipeline
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Function to extract paragraphs from a JSON file
async def extract_paragraphs_from_json(paragraphs_file: UploadFile):
    try:
        # Read JSON file
        if not paragraphs_file.filename.endswith(".json"):
            raise HTTPException(status_code=400, detail="Only JSON files are allowed.")
        paragraphs_content = await paragraphs_file.read()
        paragraphs_data = json.loads(paragraphs_content)
        paragraphs = paragraphs_data.get("paragraphs", [])
        return paragraphs
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# Response model


class ParagraphsAlignmentResponse(BaseModel):
    result: List[ParagraphAlignment] = Field(
        description="List of aligned paragraphs with their timestamps."
    )


# Endpoints

# Align with video file 
@paragraph_timestamp_router.post("/align/file")
async def align_paragraphs_with_audio(
    paragraphs_file: UploadFile = File(...),
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

        # Prepare paragraphs
        paragraphs = await extract_paragraphs_from_json(paragraphs_file=paragraphs_file)
        if not paragraphs:
            raise HTTPException(
                status_code=400, detail="No paragraphs found in the JSON file."
            )

        # Create pipeline
        transcriber_type = (
            TranscriberType.MODAL_WHISPER
            if transcriber_backend == "modal"
            else TranscriberType.FASTER_WHISPER
        )
        pipeline = get_pipeline(transcriber_type=transcriber_type)

        # Align paragraphs with audio
        result = pipeline.get_paragraphs_timestamp(
            paragraphs=paragraphs, audio=binary_audio
        )
        return ParagraphsAlignmentResponse(result=result)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the request: {str(e)}",
        )


# Align with video url 

class VideoURLrequest(BaseModel):
    media_url: str
    paragraphs: list[str]
    transcriber_backend: Optional[Literal["local", "modal"]] = Field(
        default="modal", description="Backend to run transcriber")
    

@paragraph_timestamp_router.post("/align/url")
async def align_paragraphs_with_audio(
    req: VideoURLrequest
):
    try:
        # Read media url
        media_data = read_url(url=req.media_url)
        binary_audio = io.BytesIO(media_data.content)
        
        # Create pipeline
        transcriber_type = (
            TranscriberType.MODAL_WHISPER
            if req.transcriber_backend == "modal"
            else TranscriberType.FASTER_WHISPER
        )
        pipeline = get_pipeline(transcriber_type=transcriber_type)

        # Align paragraphs with audio
        result = pipeline.get_paragraphs_timestamp(
            paragraphs=req.paragraphs, audio=binary_audio
        )
        return ParagraphsAlignmentResponse(result=result)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the request: {str(e)}",
        )


@paragraph_timestamp_router.post("/align/ass")
async def align_paragraphs_with_audio(
    paragraphs_file: UploadFile = File(...),
    ass_file: UploadFile = File(...),
):
    try:
        # Read ass file
        ass_file_content = await ass_file.read()
        ass_transcription_segments = read_ass_file(ass_file_content)

        # Prepare paragraphs
        paragraphs = await extract_paragraphs_from_json(paragraphs_file=paragraphs_file)
        if not paragraphs:
            raise HTTPException(
                status_code=400, detail="No paragraphs found in the JSON file."
            )
        
        # Create pipeline
        aligner = AlignerFactory.get_aligner(aligner_type=AlignerType.FUZZYWUZZY_ALIGNER)
        pipeline = ParagraphAssAlimentService(aligner=aligner)

        # Align paragraphs with audio
        result = pipeline.get_paragraphs_timestamp(
            paragraphs=paragraphs, ass_segments=ass_transcription_segments
        )
        return ParagraphsAlignmentResponse(result=result)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the request: {str(e)}",
        )
