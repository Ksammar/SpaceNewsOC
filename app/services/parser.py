import logging
from datetime import datetime
from typing import Any

import feedparser
from dateutil.parser import parse as parse_date
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import sync_engine
from app.models import CategoryEnum, News, Source
from app.services.classifier import classify_article, classify_with_llm

logger = logging.getLogger(__name__)

SOURCES: list[dict[str, Any]] = [
    {
        "name": "Space.com",
        "url": "https://www.space.com",
        "feed_url": "https://www.space.com/feeds/all",
        "type": "rss",
    },
    {
        "name": "NASA Breaking News",
        "url": "https://www.nasa.gov",
        "feed_url": "https://www.nasa.gov/rss/dyn/breaking_news.rss",
        "type": "rss",
    },

    {
        "name": "ESA Space Science",
        "url": "https://www.esa.int",
        "feed_url": "https://www.esa.int/rssfeed/Our_Activities/Space_Science",
        "type": "rss",
    },
    {
        "name": "SpaceNews",
        "url": "https://spacenews.com",
        "feed_url": "https://spacenews.com/feed/",
        "type": "rss",
    },
    {
        "name": "Lenta.ru Наука",
        "url": "https://lenta.ru",
        "feed_url": "https://lenta.ru/rss/news/science",
        "type": "rss",
    },
    {
        "name": "RT на русском",
        "url": "https://russian.rt.com",
        "feed_url": "https://russian.rt.com/rss",
        "type": "rss",
    },
    {
        "name": "NASASpaceFlight",
        "url": "https://www.nasaspaceflight.com",
        "feed_url": "https://www.nasaspaceflight.com/feed/",
        "type": "rss",
    },
]


def _get_or_create_source(session: Session, source_data: dict) -> Source:
    stmt = select(Source).where(Source.url == source_data["url"])
    source = session.execute(stmt).scalar_one_or_none()

    if source is None:
        source = Source(
            name=source_data["name"],
            url=source_data["url"],
            feed_url=source_data.get("feed_url"),
            type=source_data.get("type", "rss"),
        )
        session.add(source)
        session.flush()

    return source


def _parse_rss_entry(entry: Any, source: Source) -> dict | None:
    url = entry.get("link") or entry.get("id")
    if not url:
        return None

    title = (entry.get("title") or "").strip()
    if not title:
        return None

    summary = ""
    if hasattr(entry, "summary"):
        summary = entry.summary
    elif hasattr(entry, "description"):
        summary = entry.description
    summary = _clean_html(summary)

    content = ""
    if hasattr(entry, "content") and entry.content:
        content = _clean_html(entry.content[0].get("value", ""))
    if not content:
        content = summary

    image_url = _extract_image(entry)

    published_at = None
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        published_at = datetime(*entry.published_parsed[:6])
    elif hasattr(entry, "published"):
        try:
            published_at = parse_date(entry.published)
        except (ValueError, TypeError):
            published_at = datetime.now()

    return {
        "title": title,
        "url": url,
        "summary": summary[:1000] if summary else None,
        "content": content[:50000] if content else None,
        "image_url": image_url,
        "published_at": published_at,
    }


def _clean_html(text: str) -> str:
    try:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(text, "lxml")
        return soup.get_text(separator=" ", strip=True)
    except Exception:
        return text


def _extract_image(entry: Any) -> str | None:
    if hasattr(entry, "media_content") and entry.media_content:
        for media in entry.media_content:
            url = media.get("url")
            if url:
                return url

    if hasattr(entry, "links"):
        for link in entry.links:
            if link.get("type", "").startswith("image"):
                return link.get("href")

    if hasattr(entry, "summary"):
        try:
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(entry.summary, "lxml")
            img = soup.find("img")
            if img and img.get("src"):
                return img["src"]
        except Exception:
            pass

    return None


def fetch_feed(feed_url: str) -> list[dict]:
    logger.info("Fetching feed: %s", feed_url)
    try:
        feed = feedparser.parse(feed_url)
        return feed.entries
    except Exception as e:
        logger.error("Error fetching feed %s: %s", feed_url, e)
        return []


def parse_feed(feed_url: str, source: Source) -> list[dict]:
    entries = fetch_feed(feed_url)
    articles = []
    for entry in entries:
        article = _parse_rss_entry(entry, source)
        if article:
            articles.append(article)
    return articles


def _article_exists(session: Session, url: str) -> bool:
    stmt = select(News).where(News.url == url)
    return session.execute(stmt).first() is not None


def _save_article(
    session: Session,
    article: dict,
    source: Source,
    category: CategoryEnum,
) -> News | None:
    if _article_exists(session, article["url"]):
        return None

    news = News(
        title=article["title"],
        url=article["url"],
        summary=article.get("summary"),
        content=article.get("content"),
        image_url=article.get("image_url"),
        published_at=article.get("published_at"),
        category=category,
        source_id=source.id,
    )
    session.add(news)
    return news


def run_parser():
    logger.info("=" * 60)
    logger.info("Parser started at %s", datetime.now())

    with Session(sync_engine) as session:
        for source_data in SOURCES:
            source = _get_or_create_source(session, source_data)

            if not source.feed_url:
                logger.warning("Source %s has no feed_url, skipping", source.name)
                continue

            articles = parse_feed(source.feed_url, source)
            logger.info("Source %s: %d articles found", source.name, len(articles))

            for article in articles:
                text_for_classify = f"{article['title']} {article.get('summary', '')}"

                category = classify_article(text_for_classify)

                if settings.openai_api_key:
                    llm_category = classify_with_llm(
                        text_for_classify,
                        article["title"],
                        settings.openai_api_key,
                    )
                    if llm_category is not None:
                        category = llm_category

                saved = _save_article(session, article, source, category)
                if saved:
                    logger.info(
                        "  Saved: [%s] %s (%s)",
                        category.value,
                        article["title"][:80],
                        source.name,
                    )

            session.commit()

    logger.info("Parser finished at %s", datetime.now())
    logger.info("=" * 60)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_parser()
