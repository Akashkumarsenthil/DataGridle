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


@router.get("/{slug}/resources/grouped")
async def get_resources_grouped_by_week(slug: str, db: AsyncSession = Depends(get_db)):
    """Resources grouped by roadmap week and optionally by topic for the Learn tab."""
    cat = await _get_category_by_slug(slug, db)
    # Load roadmap items for this category (ordered)
    rm_result = await db.execute(
        select(RoadmapItem)
        .where(RoadmapItem.category_id == cat.id)
        .order_by(RoadmapItem.order_index)
    )
    roadmap_items = list(rm_result.scalars().all())
    rm_by_id = {r.id: r for r in roadmap_items}

    # Load all resources with topic name (left join Topic)
    from app.models.learning import LearningResource
    from app.models.topic import Topic

    res_result = await db.execute(
        select(LearningResource, Topic.name.label("topic_name"))
        .outerjoin(Topic, LearningResource.topic_id == Topic.id)
        .where(LearningResource.category_id == cat.id)
        .order_by(LearningResource.roadmap_item_id.nullslast(), LearningResource.order_in_playlist)
    )
    rows = res_result.all()

    # Build grouped: by week (roadmap_item_id)
    groups: dict[int | None, list[dict]] = {}
    for r in roadmap_items:
        groups[r.id] = []
    groups[None] = []  # resources without roadmap_item_id

    for row in rows:
        res, topic_name = row[0], row[1]
        payload = {
            "id": res.id,
            "category_id": res.category_id,
            "topic_id": res.topic_id,
            "roadmap_item_id": res.roadmap_item_id,
            "title": res.title,
            "url": res.url,
            "resource_type": res.resource_type,
            "difficulty_level": res.difficulty_level,
            "estimated_duration_minutes": res.estimated_duration_minutes,
            "order_in_playlist": res.order_in_playlist,
            "topic_name": topic_name,
        }
        rid = res.roadmap_item_id
        if rid in groups:
            groups[rid].append(payload)
        else:
            groups[None].append(payload)

    # Return list of { week_number, roadmap_title, roadmap_item_id, resources }
    out = []
    for r in roadmap_items:
        out.append({
            "week_number": r.week_number,
            "roadmap_title": r.title,
            "roadmap_item_id": r.id,
            "resources": groups.get(r.id, []),
        })
    if groups[None]:
        out.append({
            "week_number": 0,
            "roadmap_title": "Other",
            "roadmap_item_id": None,
            "resources": groups[None],
        })
    return out


@router.get("/{slug}/questions", response_model=list[QuestionResponse])
async def get_domain_questions(slug: str, db: AsyncSession = Depends(get_db)):
    cat = await _get_category_by_slug(slug, db)
    result = await db.execute(
        select(Question).where(Question.category_id == cat.id)
    )
    return result.scalars().all()


@router.get("/{slug}/roadmap/weeks/{week_number}/expand")
async def expand_roadmap_week_public(slug: str, week_number: int, db: AsyncSession = Depends(get_db)):
    """Public fallback: granular tasks and generic resources for a roadmap week (no auth, no LLM)."""
    from app.services.groq_client import build_fallback_expand_week

    cat = await _get_category_by_slug(slug, db)
    result = await db.execute(
        select(RoadmapItem)
        .where(RoadmapItem.category_id == cat.id, RoadmapItem.week_number == week_number)
        .order_by(RoadmapItem.order_index)
        .limit(1)
    )
    rm = result.scalar_one_or_none()
    if not rm:
        raise HTTPException(status_code=404, detail="Week not found")
    content = build_fallback_expand_week(rm.title, rm.description)
    return {
        "roadmap_item": {
            "id": rm.id,
            "title": rm.title,
            "description": rm.description,
            "week_number": rm.week_number,
        },
        "granular_tasks": content["granular_tasks"],
        "resources": content["resources"],
    }


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
