import whisper
from config import CAPTION_CHUNK


def _fmt(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def generate_srt(audio_path: str, srt_path: str) -> str:
    """
    Transcribe audio with word-level timestamps via Whisper.
    Groups words into CAPTION_CHUNK-sized chunks and writes an SRT file.
    Returns srt_path.
    """
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, word_timestamps=True)

    lines: list[str] = []
    idx = 1

    for segment in result["segments"]:
        words = segment.get("words", [])
        for i in range(0, len(words), CAPTION_CHUNK):
            chunk = words[i : i + CAPTION_CHUNK]
            if not chunk:
                continue
            start = chunk[0]["start"]
            end = chunk[-1]["end"]
            text = " ".join(w["word"].strip() for w in chunk).upper()
            lines.append(f"{idx}\n{_fmt(start)} --> {_fmt(end)}\n{text}\n")
            idx += 1

    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return srt_path
