# brain-rot-bot

Automated pipeline that turns trending Reddit posts into short-form "brain rot" videos and uploads them to TikTok and YouTube.

## How it works

1. Scrapes trending posts from subreddits like r/AmITheAsshole, r/tifu, r/askreddit
2. Generates a narration script via OpenAI
3. Converts script to speech (OpenAI TTS)
4. Composes video with background footage and burned-in captions
5. Uploads the finished video to TikTok and YouTube on a schedule

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # fill in your API keys
python main.py
```

## Environment variables

| Variable | Description |
|---|---|
| `REDDIT_CLIENT_ID` | Reddit API client ID |
| `REDDIT_CLIENT_SECRET` | Reddit API client secret |
| `OPENAI_API_KEY` | OpenAI API key (TTS + script generation) |
| `YOUTUBE_CLIENT_SECRETS` | Path to YouTube OAuth client secrets JSON |
| `TIKTOK_SESSION_ID` | TikTok session cookie (optional) |

## Project structure

| File | Purpose |
|---|---|
| `main.py` | Orchestrates the full pipeline and scheduler |
| `scraper.py` | Fetches trending Reddit posts |
| `tts.py` | Text-to-speech via OpenAI |
| `composer.py` | Assembles video with background + captions |
| `captions.py` | Generates SRT subtitle files |
| `uploader.py` | Uploads to YouTube and TikTok |
| `config.py` | All settings and env var loading |
