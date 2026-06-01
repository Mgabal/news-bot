"""
config.py — All settings from environment variables.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_TOKEN      = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")
ADMIN_USER_ID       = int(os.getenv("ADMIN_USER_ID", "0"))

# Groq (free AI)
GROQ_API_KEY        = os.getenv("GROQ_API_KEY", "")

# Bot behaviour
POST_INTERVAL_MINUTES = int(os.getenv("POST_INTERVAL_MINUTES", "30"))
MAX_POSTS_PER_RUN     = int(os.getenv("MAX_POSTS_PER_RUN", "3"))
