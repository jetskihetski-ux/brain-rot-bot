import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from config import YOUTUBE_CLIENT_SECRETS

_SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
_TOKEN_FILE = "token.pickle"


# ── YouTube ───────────────────────────────────────────────────────────────────

def _youtube_client():
    creds = None
    if os.path.exists(_TOKEN_FILE):
        with open(_TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                YOUTUBE_CLIENT_SECRETS, _SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(_TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)

    return build("youtube", "v3", credentials=creds)


def upload_youtube(video_path: str, title: str, description: str,
                   tags: list[str]) -> str:
    """Upload video as a YouTube Short. Returns the video ID."""
    yt = _youtube_client()

    body = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": tags,
            "categoryId": "24",          # Entertainment
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)
    req = yt.videos().insert(part=",".join(body.keys()), body=body,
                             media_body=media)

    response = None
    while response is None:
        status, response = req.next_chunk()
        if status:
            print(f"  YouTube upload: {int(status.progress() * 100)}%")

    vid_id = response["id"]
    print(f"  YouTube Shorts: https://youtube.com/shorts/{vid_id}")
    return vid_id


# ── TikTok ────────────────────────────────────────────────────────────────────
# Uses TikTok's official Content Posting API (requires approved developer access).
# Docs: https://developers.tiktok.com/doc/content-posting-api-get-started
# If you don't have API access yet, set TIKTOK_SESSION_ID=skip in .env.

import httpx
from config import TIKTOK_SESSION_ID


def upload_tiktok(video_path: str, title: str) -> str | None:
    if not TIKTOK_SESSION_ID or TIKTOK_SESSION_ID == "skip":
        print("  TikTok upload skipped (no session ID configured).")
        return None

    file_size = os.path.getsize(video_path)

    headers = {
        "Authorization": f"Bearer {TIKTOK_SESSION_ID}",
        "Content-Type": "application/json; charset=UTF-8",
    }

    # Step 1 — init upload
    init_resp = httpx.post(
        "https://open.tiktokapis.com/v2/post/publish/video/init/",
        headers=headers,
        json={
            "post_info": {
                "title": title[:150],
                "privacy_level": "PUBLIC_TO_EVERYONE",
                "disable_duet": False,
                "disable_comment": False,
                "disable_stitch": False,
            },
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": file_size,
                "chunk_size": file_size,
                "total_chunk_count": 1,
            },
        },
        timeout=30,
    )
    init_resp.raise_for_status()
    data = init_resp.json()["data"]
    upload_url = data["upload_url"]
    publish_id = data["publish_id"]

    # Step 2 — upload file
    with open(video_path, "rb") as f:
        video_bytes = f.read()

    upload_resp = httpx.put(
        upload_url,
        content=video_bytes,
        headers={
            "Content-Type": "video/mp4",
            "Content-Range": f"bytes 0-{file_size - 1}/{file_size}",
            "Content-Length": str(file_size),
        },
        timeout=120,
    )
    upload_resp.raise_for_status()

    print(f"  TikTok published (publish_id={publish_id})")
    return publish_id
