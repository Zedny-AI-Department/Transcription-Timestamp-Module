from fastapi import FastAPI
from timestamp_whisper.api.paragraph_timestamp_route import paragraph_timestamp_router


app = FastAPI()
app.include_router(paragraph_timestamp_router, tags=["Paragraphs Timestamp"])
