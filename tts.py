from openai import OpenAI
from config import OPENAI_API_KEY, TTS_MODEL, TTS_VOICE

_client = OpenAI(api_key=OPENAI_API_KEY)


def generate_audio(script: str, output_path: str) -> str:
    """Convert script to speech and save as MP3. Returns output_path."""
    response = _client.audio.speech.create(
        model=TTS_MODEL,
        voice=TTS_VOICE,
        input=script,
    )
    response.stream_to_file(output_path)
    return output_path
