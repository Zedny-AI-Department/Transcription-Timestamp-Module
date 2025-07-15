## Timestamp Module

Timestamp Whisper is a powerful FastAPI application designed to align textual paragraphs with audio or video files, generating precise timestamps for each paragraph. It leverages advanced transcription models (Faster Whisper and Modal Whisper) and fuzzy alignment techniques to provide accurate results.


---

## Features

- **Paragraph Alignment:** Align a JSON file containing paragraphs with an audio or video file.
- **Flexible Transcription Backends:** Choose between local (Faster Whisper) and cloud-based (Modal Whisper) transcription services.
- **Audio/Video Support:** Accepts both audio and video files as input.
- **FastAPI Interface:** Provides a robust and easy-to-use RESTful API.


---

## Project Structure
``` 
src/
├── api/
│   └── paragraph_timestamp_route.py
├── core/
│   ├── aligner/
│   │   ├── __init__.py
│   │   ├── fuzzy_aligner.py
|   |   └── fuzzywuzzy_aligner.py
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
│   │   ├── faster_whisper.py
|   |   └──modal_whisper.py
│   ├── types.py
├── config/
│   └── modal_app.py
├── modal_class/
│   └── modal_whisper_transcription.py
├── models/
│   ├── __init__.py
│   ├── aligner_models.py
│   └── transcription_models.py
├── services/
│   ├── __init__.py
│   └── file_chunks_timestamp_service.py
├── utils/
|   ├── __init__.py
|   ├── video_to_audio_util.py
│   └── detect_file_type_util.py
```
----

## Prerequisites
- Python 3.8+
- `uv` or `pip`
- `.env` file for environment variables

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
    MODAL_TOKEN_ID=****
    MODAL_TOKEN_SECRET=****
    MODAL_APP_NAME="***"
    MODAL_CLASS_NAME="***"
    ```

----
### Running the Application

1. Deploy modal app on modal (Optional: if you have deployed it skip this step):

    ```bash
    modal deploy src/modal_class/modal_whisper_transcription.py 
    ```
2. Run the Endpoint:
    ```bash
    uvicorn main:app --reload
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
## 📡 API Endpoints
### `POST /align`

Aligns paragraphs from a JSON file with an audio or video file and returns timestamped paragraphs.

**Request:**

- **Method:** `POST`
- **URL:** `/align`
- **Headers:** `Content-Type: multipart/form-data`
- **Form Data:**
  - `paragraphs_file`: (File) A JSON file containing a list of paragraphs under the key `"paragraphs"`.
  - `media_file`: (File) An audio or video file (e.g., `.mp3`, `.wav`, `.mp4`, `.mov`).
  - `transcriber_backend`: (Query Parameter, optional) Specifies the transcription backend to use:
    - `local` (default): Uses Faster Whisper for local transcription.
    - `modal`: Uses Modal Whisper for cloud-based transcription.


#### Example `paragraphs_file.json`

    ```json
    {
    "paragraphs": [
        "This is the first paragraph.",
        "And this is the second one, which is a bit longer.",
        "Finally, the third paragraph concludes our example."
    ]
    }
    ```
#### Example `curl` Request
    ```bash
    curl -X 'POST' \
    'http://127.0.0.1:7000/align?transcriber_backend=modal' \
    -H 'accept: application/json' \
    -H 'Content-Type: multipart/form-data' \
    -F 'paragraphs_file=@4 Know Who Are Your Customers, Main Tips To Keep These Customers (2).json;type=application/json' \
    -F 'media_file=@4 Know Who Are Your Customers, Main Tips To Keep These Customers (2).m4v;type=video/mp4'
    ```
#### #### Example `curl` Request
```json
    {
    "result": [
        {
        "paragraph": "في الفيديو ده هتعرف تحدد مين هم عملائك عشان تقدر تخافظ عليهم. في الأول إزاي هتحدد مين العملاء اللي بتتعامل معهم من الأساس؟ أول حاجة مهمة جداً ما تحطش افتراضات عن إيه اللي العميل بيفضله لإن ممكن جداً تفضيل العميل ده يتغير من وقت للتاني، فلازم وإنت بتتعامل مع العميل تتعامل مع المعلومات والبيانات اللي تعرفها عنه عشان تقدر تحدد الطرق اللي هتتعامل معاه بيها على حسب تفضيلاته مش على حسب افتراضاتك أنت.",
        "start": 0,
        "end": 30.54,
        "best_start_match": {
            "id": "2100b611-afb8-4351-a074-64a34b0ef4e0",
            "text": " في",
            "start": 0,
            "end": 0.16,
            "score": 1
        },
        "best_end_match": {
            "id": "076745da-cde5-419b-99a9-ba66b0b8f24a",
            "text": " أنت",
            "start": 30.3,
            "end": 30.54,
            "score": 0.86
        }
        },
        {
        "paragraph": "الطريقة التانية هي التعامل من خلال شبكات التواصل الاجتماعي، ودي طريقة هتساعدك جداً وهتسهل عليك التفاعل مع العملاء، وإنك تقدر تحدد أكتر عاداتهم ورغباتهم وكمان متطلباتهم في الشراء. ده غير إنه هيبقى سهل عليك تحدد بالزبط إيه هي المشاكل اللي ممكن يواجهوها. الطريقة التالتة إنك تسأل العميل، ودي من أبسط الطرق اللي ممكن تعرف بيها بشكل مباشر جداً احتياجاته، وده هيساعدك في تحديد تعاملك معاه وهيساعد الشركة كمان في إنها تطور خدمتها بشكل أفضل. أما الطريقة الرابعة فهي عمل استطلاعات للرأي، حاول إنك توصل لأكبر عدد من الملاحظات سواء كانت إيجابية أو سلبية عن الخدمة أو المنتج، لإن ده هيوفر عليك وقت كتير في فهم العميل وطريق تفكيره. يبقى كده عرفنا أربع طرق رئيسية نقدر نقيز بيهم إن احنا نحدد العميل اللي معانا.",
        "start": 30.54,
        "end": 87.02,
        "best_start_match": {
            "id": "bd24c9ba-5910-4e3a-a4d9-af62dbf51b2d",
            "text": " الطريقة",
            "start": 30.54,
            "end": 31.44,
            "score": 1
        },
        "best_end_match": {
            "id": "a1452365-6992-4cc1-b498-14c087750a10",
            "text": " معانا",
            "start": 86.66,
            "end": 87.02,
            "score": 0.91
            }
            },
            ]
    }

```
#### Error Response (400 / 500)

    ```json
        {
            "detail": "Error message describing the issue."
        }
    ```
----

## Contributing
Contributions are welcome! Please feel free to submit pull requests or open issues for any bugs or feature requests.
### Recommended Settings
----

- Use high-quality audio files for best transcription accuracy.
- Adjust model names and parameters as needed for your use case.

----
## Performance Features

- Fast and acuurate fuzzy alignment using fuzzywuzzy partial_ratio and ratio methods.
- Batch processing of paragraphs and audio segments.
- Modular design for easy scaling and extension.

----
## Error Handling
- All major operations are wrapped in try/except blocks.
- Errors during transcription or alignment raise descriptive exceptions.
- Invalid input (empty audio or paragraphs) returns empty results.
- Ensure your API keys and model names are correct to avoid authentication errors.
