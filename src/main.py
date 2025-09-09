from fastapi import FastAPI
from timestamp_whisper.api.paragraph_timestamp_route import paragraph_timestamp_router
from timestamp_whisper.api.transcriber_router import transcriber_router

app = FastAPI()
app.include_router(paragraph_timestamp_router, tags=["Paragraphs Timestamp"])
app.include_router(transcriber_router, tags=["Transcriber"])
