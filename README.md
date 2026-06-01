# 📰 Fashion & Music News Telegram Bot

Auto-posts fashion and music news to your Telegram channel every 30 minutes.
100% free — no paid APIs required.

---

## ✨ Features

- 🔄 Auto-posts every 30 minutes (configurable)
- 📰 14 RSS sources — Vogue, Billboard, Hypebeast, Rolling Stone & more
- 🤖 AI rewrites every post to sound natural (Groq free tier)
- ✅ Never reposts the same article (SQLite deduplication)
- 👗🎵 Covers Fashion + Music + Celebrity
- 🛠 Admin commands: `/status` `/postnow` `/pause` `/resume` `/feeds`
- ♻️ Easy to resell — swap feeds.py for any niche

---

## 🚀 Setup (10 minutes)

### 1. Install
```bash
pip3 install -r requirements.txt
```

### 2. Create your Telegram bot
- Message @BotFather on Telegram
- Send `/newbot` → follow prompts → copy your token

### 3. Create your Telegram channel
- Create a public or private channel
- Add your bot as an **administrator** with "Post messages" permission
- Copy the channel username (e.g. `@fashionnewschannel`)

### 4. Get your Telegram user ID
- Message @userinfobot on Telegram
- Copy your numeric ID (e.g. `123456789`)

### 5. Get a free Groq API key (optional but recommended)
- Go to console.groq.com
- Sign up free — no credit card
- Create an API key

### 6. Configure
```bash
cp .env.example .env
# Fill in TELEGRAM_TOKEN, TELEGRAM_CHANNEL_ID, ADMIN_USER_ID
# Optionally add GROQ_API_KEY for AI rewriting
```

### 7. Run
```bash
python3 main.py
```

The bot starts, immediately fetches news, and posts to your channel. ✅

---

## 🛠 Admin Commands

| Command | What it does |
|---|---|
| `/status` | Show stats — total posts, running state, feed count |
| `/postnow` | Immediately fetch & post articles (don't wait 30 min) |
| `/pause` | Stop auto-posting |
| `/resume` | Resume auto-posting |
| `/feeds` | List all active RSS feeds |

---

## 📁 Project Structure

```
news-bot/
├── main.py          # Entry point + scheduler + admin commands
├── config.py        # Settings from .env
├── requirements.txt
├── .env.example
├── bot/
│   └── poster.py    # Posts to Telegram channel
├── news/
│   ├── fetcher.py   # Pulls & filters RSS feeds
│   └── feeds.py     # All RSS URLs — edit to change niche
├── ai/
│   └── rewriter.py  # Groq AI rewrites articles → posts
└── db/
    └── models.py    # SQLite — tracks posted articles
```

---

## 🔄 Reselling to Other Niches

To deliver this bot to a different client, only change **`news/feeds.py`**:

| Client niche | What to swap |
|---|---|
| Sports news | ESPN, BBC Sport, Sky Sports RSS feeds |
| Tech news | TechCrunch, Wired, The Verge RSS |
| Crypto news | CoinDesk, CoinTelegraph RSS |
| Food/lifestyle | Eater, Food52, Bon Appétit RSS |
| Local news | Any local newspaper RSS |

Same codebase. Different feeds. Done in 5 minutes per client.

---

## ☁️ Deploy Free on Railway

1. Push to GitHub (`git push`)
2. Go to railway.app → New Project → Deploy from GitHub
3. Add your `.env` variables in the Variables tab
4. Deploy — runs 24/7 for free

---

## 💰 Selling This Bot

**Setup fee:** $150 – $350 per client
**Monthly retainer:** $30 – $60/month (hosting + maintenance)

---

## ⚠️ Note

This bot reposts public news with source attribution and links back to the original articles.
Always include source credits in posts (already done by default).
