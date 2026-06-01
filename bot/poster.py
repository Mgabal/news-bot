"""
bot/poster.py — Posts formatted articles to the Telegram channel.
"""

import logging
import asyncio
from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import TelegramError
from config import TELEGRAM_TOKEN, TELEGRAM_CHANNEL_ID

logger = logging.getLogger(__name__)


async def post_to_channel(text: str) -> bool:
    """
    Send a message to the configured Telegram channel.
    Returns True on success, False on failure.
    """
    bot = Bot(token=TELEGRAM_TOKEN)
    try:
        await bot.send_message(
            chat_id=TELEGRAM_CHANNEL_ID,
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=False,   # show link preview
        )
        return True
    except TelegramError as e:
        logger.error(f"Telegram post failed: {e}")
        return False


def post_article_sync(text: str) -> bool:
    """Synchronous wrapper for use outside async context."""
    return asyncio.run(post_to_channel(text))
