import io
import json
from typing import BinaryIO, List, Optional
from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel, Field

from src.core.types import FasterWhisperModel, TranscriberType, AlignerType
from src.core.factory.aligner_factory import AlignerFactory
from src.core.factory.transcriber_factory import TranscriberFactory
from src.models.aligner_models import ParagraphAlignment
from src.services import FileChunksTimestampService
from src.utils import convert_video_to_audio, detect_file_type


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


@paragraph_timestamp_router.post("/align")
async def align_paragraphs_with_audio(
    paragraphs_file: UploadFile = File(...), media_file: UploadFile = File(...)
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
        pipeline = get_pipeline()

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
