import io
import json
from typing import List
from typing_extensions import Annotated
from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel, Field

from src.core.types import FasterWhisperModel, TranscriberType
from src.core.factory.aligner_factory import AlignerFactory
from src.core.factory.transcriber_factory import TranscriberFactory
from src.models.aligner_models import ParagraphAlignment
from src.services import FileChunksTimestampService

paragraph_timestamp_router = APIRouter()


class ParagraphsAlignmentResponse(BaseModel):
    result: List[ParagraphAlignment] = Field(
        description="List of aligned paragraphs with their timestamps."
    )


@paragraph_timestamp_router.post("/paragraphs/timestamp")
async def align_paragraphs_with_audio(
    paragraphs_file: UploadFile = File(...),
    video_file: UploadFile = File(...)
):
    try:
        # Read paragraphs
        if not paragraphs_file.filename.endswith(".json"):
            raise HTTPException(status_code=400, detail="Only JSON files are allowed.")
        paragraphs_content = await paragraphs_file.read()
        paragraphs_data = json.loads(paragraphs_content)
        paragraphs = paragraphs_data.get("paragraphs", [])

        # Read video file
        if not paragraphs or not video_file:
            raise HTTPException(
                status_code=400, detail="Paragraphs and audio file are required."
            )
        print(f"Received {len(paragraphs)} paragraphs for alignment.")
        video_bytes = await video_file.read()
        binary_file = io.BytesIO(video_bytes)

        transcriber = TranscriberFactory.get_transcriber(
            transcriber_type=TranscriberType.FASTER_WHISPER,
            model_name=FasterWhisperModel.LARGE_V3,
        )

        aligner = AlignerFactory.get_aligner(aligner_type="fuzzy_aligner")

        pipeline = FileChunksTimestampService(
            transcriber=transcriber,
            aligner=aligner,
        )
        result = pipeline.get_paragraphs_timestamp(
            paragraphs=paragraphs, audio=binary_file
        )
        return ParagraphsAlignmentResponse(result=result)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the request: {str(e)}",
        )
