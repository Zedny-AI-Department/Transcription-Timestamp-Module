from fastapi import FastAPI
from src.api.timestamp_route import timestamp_router


app = FastAPI()
app.include_router(timestamp_router, tags=["Paragraphs Timestamp"])
