from typing import BinaryIO
import requests
from io import BytesIO
from pydantic import BaseModel, Field


class ReadURLResult(BaseModel):
    """
    Model to represent the result of reading a URL.
    """
    content: bytes = Field(..., description="The content of the URL.")
    content_type: str = Field(..., description="The content type of the URL.")

    class Config:
        arbitrary_types_allowed = True

def read_url(url: str) -> ReadURLResult:
    """
    Reads the content of a url.
    
    Args:
        url (str): The url to read.
    
    Returns:
        ReadURLResult: A model containing the content and content type of the URL.
    """
    try:
        with requests.get(url, stream=True) as data:
            data.raise_for_status()
            url_content = b""
            for chunk in data.iter_content(chunk_size=8192):
                if chunk:
                    url_content += chunk
            url_content_type = data.headers.get('Content-Type', "")
            return ReadURLResult(content=url_content, content_type=url_content_type)
    except Exception as e:
        raise Exception(f"Error while reading url: {str(e)}")
