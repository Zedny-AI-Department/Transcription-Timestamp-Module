import magic


def detect_file_type(file_bytes: bytes) -> str:
    """
    Detects the file type based on its content using the magic library.
    
    Args:
        file_bytes (bytes): The file content as bytes.
    
    Returns:
        str: The detected file type.
    """
    try:
        mime = magic.Magic(mime=True)
        return mime.from_buffer(file_bytes)  
    except Exception as e:
        raise Exception(status_code=500, detail=f"An error occurred: {str(e)}")
