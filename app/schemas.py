from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models import CategoryEnum


class NewsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    url: str
    summary: str | None
    title_ru: str | None = None
    summary_ru: str | None = None
    image_url: str | None
    published_at: datetime | None
    category: CategoryEnum
    source_name: str | None = None
    created_at: datetime


class NewsDetailResponse(NewsResponse):
    content: str | None


class SourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    url: str
    feed_url: str | None
    type: str
    is_active: bool
    created_at: datetime


class NewsListResponse(BaseModel):
    items: list[NewsResponse]
    total: int
    page: int
    pages: int
