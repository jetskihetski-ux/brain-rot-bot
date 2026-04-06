import random
import praw
from config import (
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_USER_AGENT,
    SUBREDDITS,
    MIN_WORDS,
    MAX_WORDS,
)


def _reddit() -> praw.Reddit:
    return praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT,
    )


def fetch_trending_post(used_ids: set[str] | None = None) -> dict | None:
    """
    Pull a hot text post from one of the configured subreddits.
    Skips posts already in used_ids, NSFW posts, and posts outside word limits.
    Returns a dict with id, title, text, subreddit, score, url — or None.
    """
    reddit = _reddit()
    subs = SUBREDDITS.copy()
    random.shuffle(subs)

    for sub in subs:
        for post in reddit.subreddit(sub).hot(limit=30):
            if not post.is_self or post.over_18:
                continue
            word_count = len(post.selftext.split())
            if not (MIN_WORDS <= word_count <= MAX_WORDS):
                continue
            if used_ids and post.id in used_ids:
                continue
            return {
                "id": post.id,
                "title": post.title,
                "text": post.selftext,
                "subreddit": sub,
                "score": post.score,
                "url": f"https://reddit.com{post.permalink}",
            }

    return None


def build_script(post: dict) -> str:
    """Format post into a narration script."""
    return (
        f"{post['title']}. "
        f"Posted on r slash {post['subreddit']}. "
        f"{post['text']}"
    )
