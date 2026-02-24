from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.category import Category
from app.models.topic import Topic
from app.models.daily_question import DailyQuestion
from app.models.roadmap import RoadmapItem
from app.models.learning import LearningResource
from app.models.question import Question
from app.schemas.category import (
    CategoryResponse,
    TopicResponse,
    RoadmapItemResponse,
    LearningResourceResponse,
)
from app.schemas.question import QuestionResponse

router = APIRouter(prefix="/categories", tags=["Categories"])


async def _get_category_by_slug(slug: str, db: AsyncSession) -> Category:
    result = await db.execute(select(Category).where(Category.slug == slug))
    cat = result.scalar_one_or_none()
    if not cat:
        raise HTTPException(status_code=404, detail="Domain not found")
    return cat


@router.get("/", response_model=list[CategoryResponse])
async def list_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category))
    return result.scalars().all()


@router.get("/{slug}/detail", response_model=CategoryResponse)
async def get_category_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    return await _get_category_by_slug(slug, db)


@router.get("/{category_id}/topics", response_model=list[TopicResponse])
async def list_topics(category_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Topic)
        .where(Topic.category_id == category_id)
        .order_by(Topic.order_index)
    )
    return result.scalars().all()


@router.get("/{slug}/roadmap", response_model=list[RoadmapItemResponse])
async def get_roadmap(slug: str, db: AsyncSession = Depends(get_db)):
    cat = await _get_category_by_slug(slug, db)
    result = await db.execute(
        select(RoadmapItem)
        .where(RoadmapItem.category_id == cat.id)
        .order_by(RoadmapItem.order_index)
    )
    return result.scalars().all()


@router.get("/{slug}/resources", response_model=list[LearningResourceResponse])
async def get_resources(slug: str, db: AsyncSession = Depends(get_db)):
    cat = await _get_category_by_slug(slug, db)
    result = await db.execute(
        select(LearningResource)
        .where(LearningResource.category_id == cat.id)
        .order_by(LearningResource.order_in_playlist)
    )
    return result.scalars().all()


@router.get("/{slug}/questions", response_model=list[QuestionResponse])
async def get_domain_questions(slug: str, db: AsyncSession = Depends(get_db)):
    cat = await _get_category_by_slug(slug, db)
    result = await db.execute(
        select(Question).where(Question.category_id == cat.id)
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
