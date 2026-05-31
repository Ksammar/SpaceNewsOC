from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models import Source
from app.schemas import SourceResponse

router = APIRouter(prefix="/api/sources", tags=["Sources"])


@router.get("", response_model=list[SourceResponse])
async def get_sources(
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    result = await session.execute(select(Source).where(Source.is_active == True))
    sources = result.scalars().all()
    return [SourceResponse.model_validate(s) for s in sources]
