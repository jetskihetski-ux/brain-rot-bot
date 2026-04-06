import json
import os
import schedule
import time
from datetime import date
from pathlib import Path

from captions import generate_srt
from composer import compose_video
from config import OUTPUT_DIR, UPLOAD_TIME
from scraper import build_script, fetch_trending_post
from tts import generate_audio
from uploader import upload_tiktok, upload_youtube

_USED_IDS_FILE = "used_ids.json"


def _load_used() -> set[str]:
    if os.path.exists(_USED_IDS_FILE):
        with open(_USED_IDS_FILE) as f:
            return set(json.load(f))
    return set()


def _save_used(post_id: str) -> None:
    ids = _load_used()
    ids.add(post_id)
    with open(_USED_IDS_FILE, "w") as f:
        json.dump(list(ids), f)


def run_pipeline() -> None:
    print(f"\n[{date.today()}] Starting pipeline...")
    Path(OUTPUT_DIR).mkdir(exist_ok=True)

    # 1. Fetch post
    post = fetch_trending_post(used_ids=_load_used())
    if not post:
        print("No suitable post found — skipping today.")
        return
    print(f"Post: {post['title'][:70]}...")

    pid = post["id"]
    audio_path = f"{OUTPUT_DIR}/{pid}.mp3"
    srt_path   = f"{OUTPUT_DIR}/{pid}.srt"
    video_path = f"{OUTPUT_DIR}/{pid}.mp4"

    # 2. TTS
    print("Generating audio...")
    generate_audio(build_script(post), audio_path)

    # 3. Captions
    print("Generating captions...")
    generate_srt(audio_path, srt_path)

    # 4. Compose video
    print("Composing video...")
    compose_video(audio_path, srt_path, video_path)

    # 5. Upload
    title       = f"{post['title'][:90]} #shorts"
    description = f"r/{post['subreddit']} | {post['url']}"
    tags        = ["shorts", "reddit", "storytime", post["subreddit"], "brainrot"]

    print("Uploading...")
    upload_youtube(video_path, title, description, tags)
    upload_tiktok(video_path, title)

    _save_used(pid)
    print("Done!")


if __name__ == "__main__":
    run_pipeline()                                          # run once immediately
    schedule.every().day.at(UPLOAD_TIME).do(run_pipeline)  # then daily

    while True:
        schedule.run_pending()
        time.sleep(60)
