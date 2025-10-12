from typing import List
import uuid

from timestamp_whisper.models.transcription_models import SegmentTranscriptionModel


def read_ass_file(content_bytes: str) -> List[SegmentTranscriptionModel]:
    """
    Parses the content of an ASS (Advanced SubStation Alpha) subtitle file and extracts subtitle events.
    Args:
        content_bytes (str): The byte content of the ASS file.
    Returns:
        List[SegmentTranscriptionModel]: A list of models, each containing 'start', 'end', and 'text' keys representing
                    the start time, end time, and subtitle text for each dialogue event.
    """
    try:
        subtitles = []
        in_events_section = False

        content_str = content_bytes.decode("utf-8-sig")
        for line in content_str.splitlines():
            line = line.strip()

            if line.startswith('[Events]'):
                in_events_section = True
                continue

            if in_events_section:
                if line.startswith('Format:'):
                    continue  # skip the format line
                elif line.startswith('Dialogue:'):
                    parts = line.split(',', 9)  # split into 10 parts max
                    if len(parts) >= 10:
                        start_sec = ass_time_to_seconds(parts[1])
                        end_sec = ass_time_to_seconds(parts[2])
                        text = parts[9].replace('\n', ' ')  # ASS uses \N for line breaks
                        subtitles.append(
                            SegmentTranscriptionModel(
                                start=float(start_sec), end=float(end_sec), text=text, id=str(uuid.uuid4())
                            )
                        )
        return subtitles
    except Exception as e:
        raise Exception(f"Error while extracting transcription segments from ass file; {str(e)}")


def ass_time_to_seconds(time_str: str) -> float:
    """
    Converts an ASS subtitle time string to seconds.
    The input time string should be in the format 'H:MM:SS.CC', where:
        - H: hours
        - MM: minutes
        - SS: seconds
        - CC: centiseconds
    Args:
        time_str (str): Time string in ASS format.
    Returns:
        float: The time in seconds.
    Example:
        >>> ass_time_to_seconds("1:02:03.45")
        3723.45
    """

    # Format: H:MM:SS.CC
    h, m, s = time_str.split(':')
    s, cs = s.split('.')
    return int(h) * 3600 + int(m) * 60 + int(s) + int(cs) / 100.0