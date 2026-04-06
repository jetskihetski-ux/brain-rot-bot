import random
from pathlib import Path

import ffmpeg

from config import BACKGROUNDS_DIR, VIDEO_WIDTH, VIDEO_HEIGHT


def _pick_background() -> str:
    videos = list(Path(BACKGROUNDS_DIR).glob("*.mp4"))
    if not videos:
        raise FileNotFoundError(
            f"No .mp4 files found in {BACKGROUNDS_DIR}/\n"
            "Add gameplay footage (Minecraft, Subway Surfers, etc.) to that folder."
        )
    return str(random.choice(videos))


def compose_video(audio_path: str, srt_path: str, output_path: str) -> str:
    """
    Build the final 9:16 short:
      - Random background video (looped to audio length)
      - TTS audio track
      - Burned-in captions (large, bold, centre-screen)
    Returns output_path.
    """
    bg = _pick_background()

    # Measure audio duration
    probe = ffmpeg.probe(audio_path)
    duration = float(probe["format"]["duration"])

    # Caption style — big white bold text with black outline
    caption_style = (
        "FontName=Arial,"
        "FontSize=22,"
        "Bold=1,"
        "PrimaryColour=&H00FFFFFF,"
        "OutlineColour=&H00000000,"
        "BorderStyle=1,"
        "Outline=3,"
        "Shadow=0,"
        "Alignment=2,"   # centred, bottom anchor
        "MarginV=500"    # push up to centre-ish of screen
    )

    video = (
        ffmpeg
        .input(bg, stream_loop=-1, t=duration)
        .video
        .filter("scale", VIDEO_WIDTH, VIDEO_HEIGHT,
                force_original_aspect_ratio="fill")
        .filter("crop", VIDEO_WIDTH, VIDEO_HEIGHT)
        .filter("subtitles", srt_path, force_style=caption_style)
    )

    audio = ffmpeg.input(audio_path).audio

    (
        ffmpeg
        .output(
            video, audio, output_path,
            vcodec="libx264",
            acodec="aac",
            pix_fmt="yuv420p",
            video_bitrate="4M",
            audio_bitrate="192k",
            t=duration,
        )
        .overwrite_output()
        .run(quiet=True)
    )

    return output_path
