"""
main.py — Entry point.

Starts the Telegram bot with admin commands AND
runs the background scheduler that auto-posts news.

Admin commands (only work for ADMIN_USER_ID):
  /status    — show bot stats (articles posted, paused state)
  /postnow   — immediately fetch and post up to MAX_POSTS_PER_RUN articles
  /pause     — pause auto-posting
  /resume    — resume auto-posting
  /feeds     — list all active RSS feeds
"""

import logging
import asyncio
from datetime import datetime

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import TELEGRAM_TOKEN, ADMIN_USER_ID, POST_INTERVAL_MINUTES, MAX_POSTS_PER_RUN
from db.models import init_db, is_posted, mark_posted, get_state, set_state, Session, PostedArticle
from news.fetcher import fetch_all_articles
from news.feeds import FEEDS
from ai.rewriter import format_post
from bot.poster import post_to_channel

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ── Core posting job ──────────────────────────────────────────────

async def run_posting_job(context: ContextTypes.DEFAULT_TYPE = None, bot=None):
    """Fetch new articles and post up to MAX_POSTS_PER_RUN to the channel."""

    if get_state("paused") == "true":
        logger.info("Bot is paused — skipping posting job.")
        return

    logger.info("Running posting job...")
    articles = fetch_all_articles()
    posted_count = 0

    for article in articles:
        if posted_count >= MAX_POSTS_PER_RUN:
            break

        if is_posted(article["link"]):
            continue

        text = format_post(article)

        # Use passed bot or context bot
        _bot = bot or (context.bot if context else None)
        if not _bot:
            logger.error("No bot instance available.")
            break

        from config import TELEGRAM_CHANNEL_ID
        from telegram.constants import ParseMode
        try:
            await _bot.send_message(
                chat_id=TELEGRAM_CHANNEL_ID,
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=False,
            )
            mark_posted(article)
            posted_count += 1
            logger.info(f"Posted: {article['title'][:60]}")

            # Small delay between posts so they don't spam
            await asyncio.sleep(3)

        except Exception as e:
            logger.error(f"Failed to post '{article['title'][:40]}': {e}")

    logger.info(f"Posting job done. Posted {posted_count} article(s).")


# ── Admin command helpers ─────────────────────────────────────────

def admin_only(func):
    """Decorator — rejects non-admin users."""
    async def wrapper(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != ADMIN_USER_ID:
            await update.message.reply_text("⛔ Admin only.")
            return
        return await func(update, ctx)
    return wrapper


# ── Admin commands ────────────────────────────────────────────────

@admin_only
async def cmd_status(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    session = Session()
    total = session.query(PostedArticle).count()
    paused = get_state("paused") == "true"
    status = "⏸ Paused" if paused else "▶️ Running"

    await update.message.reply_text(
        f"📊 *Bot Status*\n\n"
        f"State: {status}\n"
        f"Total articles posted: `{total}`\n"
        f"Post interval: every `{POST_INTERVAL_MINUTES}` minutes\n"
        f"Max posts per run: `{MAX_POSTS_PER_RUN}`\n"
        f"Active feeds: `{len(FEEDS)}`",
        parse_mode="Markdown"
    )


@admin_only
async def cmd_postnow(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Fetching and posting now...")
    await run_posting_job(context=ctx)
    await update.message.reply_text("✅ Done!")


@admin_only
async def cmd_pause(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    set_state("paused", "true")
    await update.message.reply_text("⏸ Auto-posting *paused*.", parse_mode="Markdown")


@admin_only
async def cmd_resume(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    set_state("paused", "false")
    await update.message.reply_text("▶️ Auto-posting *resumed*.", parse_mode="Markdown")


@admin_only
async def cmd_feeds(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lines = ["📡 *Active RSS Feeds*\n"]
    for f in FEEDS:
        emoji = "👗" if f["category"] == "fashion" else "🎵" if f["category"] == "music" else "⭐"
        lines.append(f"{emoji} `{f['name']}` — {f['category']}")
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


# ── Main ──────────────────────────────────────────────────────────

async def post_init(app: Application):
    """Called after the event loop is running — safe to start scheduler here."""
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        run_posting_job,
        "interval",
        minutes=POST_INTERVAL_MINUTES,
        next_run_time=datetime.now(),
        kwargs={"bot": app.bot},
    )
    scheduler.start()
    logger.info(f"Scheduler started — posting every {POST_INTERVAL_MINUTES} minutes.")


def main():
    init_db()
    logger.info("Database ready.")

    app = (
        Application.builder()
        .token(TELEGRAM_TOKEN)
        .post_init(post_init)
        .build()
    )

    # Register admin commands
    app.add_handler(CommandHandler("status",  cmd_status))
    app.add_handler(CommandHandler("postnow", cmd_postnow))
    app.add_handler(CommandHandler("pause",   cmd_pause))
    app.add_handler(CommandHandler("resume",  cmd_resume))
    app.add_handler(CommandHandler("feeds",   cmd_feeds))

    logger.info("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
