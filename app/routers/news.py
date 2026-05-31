import math
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database import get_async_session
from app.models import CategoryEnum, News, Source
from app.schemas import NewsDetailResponse, NewsListResponse, NewsResponse

router = APIRouter(prefix="/api/news", tags=["News"])

PER_PAGE = 20


def _news_to_response(news: News) -> NewsResponse:
    return NewsResponse(
        id=news.id,
        title=news.title,
        url=news.url,
        summary=news.summary,
        title_ru=news.title_ru,
        summary_ru=news.summary_ru,
        image_url=news.image_url,
        published_at=news.published_at,
        category=news.category,
        source_name=news.source.name if news.source else None,
        created_at=news.created_at,
    )


@router.get("", response_model=NewsListResponse)
async def get_news(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    page: int = Query(1, ge=1),
    category: CategoryEnum | None = Query(None),
):
    query = select(News).options(joinedload(News.source))

    count_query = select(func.count(News.id))

    if category:
        query = query.where(News.category == category)
        count_query = count_query.where(News.category == category)

    total = (await session.execute(count_query)).scalar() or 0
    pages = max(1, math.ceil(total / PER_PAGE))

    query = (
        query
        .order_by(News.published_at.desc().nullslast(), News.id.desc())
        .offset((page - 1) * PER_PAGE)
        .limit(PER_PAGE)
    )

    result = await session.execute(query)
    news_list = result.scalars().unique().all()

    return NewsListResponse(
        items=[_news_to_response(n) for n in news_list],
        total=total,
        page=page,
        pages=pages,
    )


@router.get("/{news_id}", response_model=NewsDetailResponse)
async def get_news_by_id(
    news_id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    query = (
        select(News)
        .options(joinedload(News.source))
        .where(News.id == news_id)
    )
    result = await session.execute(query)
    news = result.scalar_one_or_none()

    if not news:
        raise HTTPException(status_code=404, detail="News not found")

    base = _news_to_response(news)
    return NewsDetailResponse(
        **base.model_dump(),
        content=news.content,
    )
