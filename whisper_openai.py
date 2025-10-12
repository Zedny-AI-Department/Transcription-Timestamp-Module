import json
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
file_path = "تخيل تحفظ المنهج في ٤ ايام فقط .mp4"
audio_file = open(file_path, "rb")

transcription = client.audio.transcriptions.create(
    model="whisper-3",
    response_format="verbose_json",
    timestamp_granularities=["segment"],
    file=audio_file
)

print(f'result: {transcription}')
segments_info = {"result": []}
for segment in transcription.segments:
    segments_info['result'].append({
    "id": segment.id,
    "text": segment.text,
    "start": segment.start,
    "end": segment.end
    }
    )
with open("output.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(segments_info))
