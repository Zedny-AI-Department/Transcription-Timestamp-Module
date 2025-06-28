from typing import List
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.params import Depends, Form
from pydantic import BaseModel, Field

from src.core.factory.aligner_factory import AlignerFactory
from src.core.factory.transcriber_factory import TranscriberFactory
from src.models.aligner_models import ParagraphAlignment
from src.pipeline import FileChunksTimestampPipeline

timestamp_router = APIRouter()


class UploadParagraphsRequest(BaseModel):
    paragraphs: List[str]


class ParagraphsAlignmentResponse(BaseModel):
    result: List[ParagraphAlignment] = Field(
        description="List of aligned paragraphs with their timestamps."
        )
    
# Dependency to parse the form data
def get_upload_data(paragraphs: str = Form(...)) -> UploadParagraphsRequest:
    try:
        split_paragraphs = [p.strip() for p in paragraphs.split(",")]
        return UploadParagraphsRequest(paragraphs=split_paragraphs)
    except Exception as e:
        raise ValueError("Invalid labels JSON", str(e))
    


@timestamp_router.post("/timestamp")
def align_paragraphs_with_audio(
    paragraphs: UploadParagraphsRequest = Depends(get_upload_data),
    file: UploadFile = File(...)
):
    try:
        if not paragraphs.paragraphs or not file:
            raise HTTPException(
                status_code=400,
                detail="Paragraphs and audio file are required."
            )
        transcriber = TranscriberFactory.get_transcriber(
            transcriber_type="whisper_fireworks",
        )

        aligner = AlignerFactory.get_aligner(aligner_type="fuzzy_aligner")

        pipeline = FileChunksTimestampPipeline(
            transcriber=transcriber,
            aligner=aligner,
        )
        result = pipeline.get_paragraphs_timestamp(
            paragraphs=paragraphs.paragraphs,
            audio=file.file
        )
        return ParagraphsAlignmentResponse(result=result)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the request: {str(e)}"
        )