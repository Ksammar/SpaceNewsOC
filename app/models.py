import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class CategoryEnum(str, enum.Enum):
    russia = "russia"
    science = "science"
    private = "private"


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    feed_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="rss"
    )
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    news: Mapped[list["News"]] = relationship("News", back_populates="source")

    def __repr__(self):
        return f"<Source(id={self.id}, name={self.name!r})>"


class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    url: Mapped[str] = mapped_column(
        String(1000), nullable=False, unique=True, index=True
    )
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    title_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    summary_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    published_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    category: Mapped[CategoryEnum] = mapped_column(
        Enum(CategoryEnum, name="category_enum"),
        nullable=False,
        index=True,
    )
    source_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("sources.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    source: Mapped["Source"] = relationship("Source", back_populates="news")

    def __repr__(self):
        return f"<News(id={self.id}, title={self.title!r}, category={self.category})>"
