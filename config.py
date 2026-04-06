import os
from dotenv import load_dotenv

load_dotenv()

# Reddit
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "brain-rot-bot/1.0")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# YouTube
YOUTUBE_CLIENT_SECRETS = os.getenv("YOUTUBE_CLIENT_SECRETS", "client_secrets.json")

# TikTok (optional)
TIKTOK_SESSION_ID = os.getenv("TIKTOK_SESSION_ID")

# Content settings
SUBREDDITS = ["AmITheAsshole", "tifu", "askreddit", "confession", "relationship_advice"]
MIN_WORDS = 150
MAX_WORDS = 400

# TTS
TTS_VOICE = "nova"   # alloy | echo | fable | onyx | nova | shimmer
TTS_MODEL = "tts-1"

# Video
BACKGROUNDS_DIR = "assets/backgrounds"
OUTPUT_DIR = "output"
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
CAPTION_CHUNK = 4       # words per caption line

# Schedule
UPLOAD_TIME = "10:00"   # daily upload time (24h)
