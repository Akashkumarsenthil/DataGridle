from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.category import Category
from app.models.topic import Topic
from app.models.daily_question import DailyQuestion
from app.schemas.category import CategoryResponse, TopicResponse
from app.schemas.question import QuestionResponse

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[CategoryResponse])
async def list_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category))
    return result.scalars().all()


@router.get("/{category_id}/topics", response_model=list[TopicResponse])
async def list_topics(category_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Topic)
        .where(Topic.category_id == category_id)
        .order_by(Topic.order_index)
    )
    return result.scalars().all()


@router.get("/{category_id}/daily-question", response_model=QuestionResponse)
async def get_daily_question(category_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(DailyQuestion)
        .where(DailyQuestion.category_id == category_id, DailyQuestion.date == date.today())
    )
    daily = result.scalar_one_or_none()
    if not daily:
        raise HTTPException(status_code=404, detail="No daily question set for today")
    return daily.question
