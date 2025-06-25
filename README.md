## Timestamp Module

A modular pipeline for audio transcription and paragraph timestamp alignment using state-of-the-art models and fuzzy matching. This module enables you to transcribe audio files, align text paragraphs with audio segments, and retrieve precise timestamps for each paragraph.

---

## Features

- **Audio Transcription:** Supports segment-level and word-level transcription using Whisper.
- **Paragraph Alignment:** Aligns text paragraphs with transcribed audio segments.
- **Extensible Factory Pattern:** Easily add new transcribers or aligners.
- **Typed Models:** Uses Pydantic for robust data validation.
- **Environment Configuration:** Supports `.env` for API keys and settings.
- **Error Handling:** Graceful error reporting for failed transcriptions or alignments.

---

## Project Structure
``` 
src/
├── core/
│   ├── aligner/
│   │   ├── __init__.py
│   │   └── fuzzy_aligner.py
│   ├── factory/
│   │   ├── __init__.py
│   │   ├── aligner_factory.py
│   │   └── transcriber_factory.py
│   ├── interface/
│   │   ├── __init__.py
│   │   ├── aligner_interface.py
│   │   └── transcriber_interface.py
│   ├── transcriber/
│   │   ├── __init__.py
│   │   ├── whisper_fireworks.py
│   │   └── types.py
├── models/
│   ├── __init__.py
│   ├── aligner_models.py
│   └── transcription_models.py
├── pipeline/
│   ├── __init__.py
│   └── file_chunks_timestamp_pipeline.py
```
----

## Prerequisites
- Python 3.8+
- `uv` or `pip`
- Fireworks API key (for Whisper Fireworks transcription)
- (Optional) `.env` file for environment variables

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-org/timestamo_whisper.git
   cd timestamo_whisper
    ```

2. Install dependencies:

    ```bash
   pip install -r requirements.txt
    ```

3. Set up environment variables:
    - Create a .env file in the root directory:

    ```bash
    FIREWORKS_API=your_fireworks_api_key
    ```

----
### Running the Application

You can integrate the pipeline in your Python code as follows:

    ```
    from src.core.factory.transcriber_factory import TranscriberFactory
    from src.core.factory.aligner_factory import AlignerFactory
    from src.pipeline.file_chunks_timestamp_pipeline import FileChunksTimestampPipeline

    # Initialize transcriber and aligner
    transcriber = TranscriberFactory.get_transcriber("whisper_fireworks")
    aligner = AlignerFactory.get_aligner("fuzzy_aligner")

    # Create pipeline
    pipeline = FileChunksTimestampPipeline(transcriber, aligner)

    # Example usage
    paragraphs = ["First paragraph...", "Second paragraph..."]
    with open("audio_file.wav", "rb") as f:
        audio_bytes = f.read()

    timestamps = pipeline.get_paragraphs_timestamp(paragraphs, audio_bytes)
    print(timestamps)
    ```

-----
## Module Documentation

### Transcriber Interface

- transcribe_segments_timestamp(audio: bytes, model_name: str, **kwargs) -> List[TranscribedChunk]
- transcribe_words_timestamp(audio: bytes, model_name: str, **kwargs) -> List[TranscribedChunk]


### Aligner Interface

- align_paragraph_timestamp_with_segments(paragraph: str, segments: List[TranscribedChunk], **kwargs) -> ParagraphAlignment

### Pipeline
- get_paragraphs_timestamp(paragraphs: List[str], audio: bytes, transcriber_model: str) -> List[ParagraphAlignment]

----
### Recommended Settings

- Use high-quality audio files for best transcription accuracy.
- Set your Fireworks API key in the .env file.
- Adjust model names and parameters as needed for your use case.

----
## Performance Features

- Fast fuzzy alignment using Levenshtein ratio.
- Batch processing of paragraphs and audio segments.
- Modular design for easy scaling and extension.

----
## Error Handling
- All major operations are wrapped in try/except blocks.
- Errors during transcription or alignment raise descriptive exceptions.
- Invalid input (empty audio or paragraphs) returns empty results.
- Ensure your API keys and model names are correct to avoid authentication errors.
