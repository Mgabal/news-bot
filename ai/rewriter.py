"""
ai/rewriter.py — Rewrites raw articles into engaging Telegram posts.

Uses Groq's free API (llama-3.1-8b-instant model).
Falls back to a clean manual formatter if Groq is unavailable.
100% free.
"""

import logging
import re
from config import GROQ_API_KEY

logger = logging.getLogger(__name__)

# Emoji sets per category
CATEGORY_EMOJIS = {
    "fashion":   ["✨", "👗", "💅", "🔥", "👠", "💎", "🕶️", "👜"],
    "music":     ["🎵", "🎤", "🔥", "🎶", "🎸", "🏆", "💿", "🎧"],
    "celebrity": ["⭐", "🔥", "💫", "📸", "👑", "🌟", "💬", "🎬"],
}

CATEGORY_HASHTAGS = {
    "fashion": ["#Fashion", "#Style", "#Trend", "#OOTD", "#FashionNews", "#Designer", "#Luxury"],
    "music":   ["#Music", "#NewMusic", "#MusicNews", "#Artist", "#NewRelease", "#Chart"],
    "celebrity": ["#Celebrity", "#Entertainment", "#PopCulture", "#Famous", "#News"],
}


def _pick_emojis(category: str, count: int = 2) -> str:
    import random
    pool = CATEGORY_EMOJIS.get(category, ["🔥", "⭐"])
    return " ".join(random.sample(pool, min(count, len(pool))))


def _pick_hashtags(category: str, count: int = 4) -> str:
    import random
    pool = CATEGORY_HASHTAGS.get(category, ["#News"])
    return " ".join(random.sample(pool, min(count, len(pool))))


def _manual_format(article: dict) -> str:
    """
    Fallback formatter — no AI needed.
    Produces a clean, readable Telegram post from raw article data.
    """
    emojis   = _pick_emojis(article["category"])
    hashtags = _pick_hashtags(article["category"])

    # Clean up summary — strip HTML tags
    summary = re.sub(r"<[^>]+>", "", article.get("summary", "")).strip()
    if len(summary) > 280:
        summary = summary[:277] + "..."

    lines = [
        f"{emojis} *{article['title']}*",
        "",
    ]
    if summary:
        lines.append(summary)
        lines.append("")

    lines += [
        f"📰 Source: {article['source']}",
        f"🔗 [Read more]({article['link']})",
        "",
        hashtags,
    ]

    return "\n".join(lines)


def rewrite_with_groq(article: dict) -> str:
    """
    Use Groq's free LLM to rewrite the article into an engaging post.
    Falls back to _manual_format() on any error.
    """
    if not GROQ_API_KEY:
        logger.info("No Groq key — using manual formatter.")
        return _manual_format(article)

    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)

        prompt = f"""You are a social media editor for a Telegram channel about {article['category']} news.

Rewrite the following article into an engaging, punchy Telegram post.

Rules:
- Start with 1-2 relevant emojis
- Write 2-3 short, engaging sentences. No fluff.
- End with 3-5 relevant hashtags
- Use *bold* for the most important phrase
- Do NOT include a URL — it will be added separately
- Keep total length under 300 characters (excluding hashtags)
- Sound like a real human editor, not a robot

Article title: {article['title']}
Article summary: {article.get('summary', '')[:400]}
Category: {article['category']}
Source: {article['source']}

Write ONLY the Telegram post text, nothing else."""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # Groq's fastest free model
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.8,
        )

        ai_text = response.choices[0].message.content.strip()

        # Append source + link after AI text
        full_post = (
            f"{ai_text}\n\n"
            f"📰 {article['source']}\n"
            f"🔗 [Read more]({article['link']})"
        )
        return full_post

    except Exception as e:
        logger.warning(f"Groq rewrite failed ({e}), using manual formatter.")
        return _manual_format(article)


def format_post(article: dict) -> str:
    """Main entry point — always returns a ready-to-post string."""
    return rewrite_with_groq(article)
