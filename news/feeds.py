"""
news/feeds.py — All RSS feed sources.

To resell to a different niche client, just swap these feeds.
Each feed has a category tag used for hashtag generation.
"""

FEEDS = [

    # ── FASHION ──────────────────────────────────────────────────
    {
        "name": "Vogue",
        "url": "https://www.vogue.com/feed/rss",
        "category": "fashion",
    },
    {
        "name": "Hypebeast",
        "url": "https://hypebeast.com/feed",
        "category": "fashion",
    },
    {
        "name": "Harper's Bazaar",
        "url": "https://www.harpersbazaar.com/rss/all.xml/",
        "category": "fashion",
    },
    {
        "name": "Elle",
        "url": "https://www.elle.com/rss/all.xml/",
        "category": "fashion",
    },
    {
        "name": "WWD Fashion",
        "url": "https://wwd.com/feed/",
        "category": "fashion",
    },
    {
        "name": "Google News Fashion",
        "url": "https://news.google.com/rss/search?q=fashion+brands+designer&hl=en-US&gl=US&ceid=US:en",
        "category": "fashion",
    },
    {
        "name": "Google News Luxury Fashion",
        "url": "https://news.google.com/rss/search?q=Gucci+OR+Dior+OR+Chanel+OR+Prada+OR+LV&hl=en-US&gl=US&ceid=US:en",
        "category": "fashion",
    },

    # ── MUSIC & CELEBRITY ─────────────────────────────────────────
    {
        "name": "Billboard",
        "url": "https://www.billboard.com/feed/",
        "category": "music",
    },
    {
        "name": "Rolling Stone",
        "url": "https://www.rollingstone.com/feed/",
        "category": "music",
    },
    {
        "name": "NME",
        "url": "https://www.nme.com/feed",
        "category": "music",
    },
    {
        "name": "Pitchfork",
        "url": "https://pitchfork.com/rss/news/",
        "category": "music",
    },
    {
        "name": "Google News Music",
        "url": "https://news.google.com/rss/search?q=music+celebrity+artist+new+release&hl=en-US&gl=US&ceid=US:en",
        "category": "music",
    },
    {
        "name": "Google News Celebrity",
        "url": "https://news.google.com/rss/search?q=celebrity+news+today&hl=en-US&gl=US&ceid=US:en",
        "category": "celebrity",
    },
]

# Keywords to filter articles — only post if title/summary contains one of these
FASHION_KEYWORDS = [
    "fashion", "style", "designer", "collection", "runway", "brand",
    "outfit", "wear", "trend", "luxury", "gucci", "dior", "chanel",
    "prada", "versace", "balenciaga", "louis vuitton", "zara", "h&m",
    "streetwear", "couture", "vogue", "lookbook", "collaboration",
]

MUSIC_KEYWORDS = [
    "music", "album", "song", "single", "tour", "concert", "artist",
    "rapper", "singer", "band", "release", "chart", "billboard",
    "Grammy", "award", "celebrity", "taylor swift", "beyoncé", "drake",
    "travis scott", "rihanna", "new track", "debut", "collab",
]

ALL_KEYWORDS = FASHION_KEYWORDS + MUSIC_KEYWORDS
