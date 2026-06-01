"""
db/models.py — Tracks posted articles to prevent duplicates.
"""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///news_bot.db", connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)


class PostedArticle(Base):
    __tablename__ = "posted_articles"

    id         = Column(Integer, primary_key=True)
    url        = Column(String, unique=True, nullable=False)
    title      = Column(String)
    source     = Column(String)
    category   = Column(String)
    posted_at  = Column(DateTime, default=datetime.utcnow)


class BotState(Base):
    __tablename__ = "bot_state"

    id      = Column(Integer, primary_key=True)
    key     = Column(String, unique=True, nullable=False)
    value   = Column(String, default="")


def init_db():
    Base.metadata.create_all(engine)


def is_posted(url: str) -> bool:
    session = Session()
    return session.query(PostedArticle).filter_by(url=url).first() is not None


def mark_posted(article: dict):
    session = Session()
    record = PostedArticle(
        url=article["link"],
        title=article["title"],
        source=article["source"],
        category=article["category"],
    )
    session.add(record)
    session.commit()


def get_state(key: str, default: str = "") -> str:
    session = Session()
    row = session.query(BotState).filter_by(key=key).first()
    return row.value if row else default


def set_state(key: str, value: str):
    session = Session()
    row = session.query(BotState).filter_by(key=key).first()
    if row:
        row.value = value
    else:
        session.add(BotState(key=key, value=value))
    session.commit()
