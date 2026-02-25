from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.submission import Submission
from app.models.progress import UserProgress
from app.models.badge import UserBadge, Badge
from app.models.assessment import UserTopicStrength
from app.models.topic import Topic
from app.models.category import Category
from app.models.domain_preference import UserDomainPreference
from app.schemas.user import UserResponse, UserProfileUpdate, DomainPreferenceResponse, DomainPreferenceUpdate
from app.schemas.question import SubmissionResponse
from app.schemas.assessment import UserProfileWithStrengthsResponse, TopicStrengthResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me/profile", response_model=UserProfileWithStrengthsResponse)
async def get_my_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Current user's profile with topic strengths (from onboarding assessment)."""
    result = await db.execute(
        select(UserTopicStrength, Topic, Category)
        .join(Topic, UserTopicStrength.topic_id == Topic.id)
        .join(Category, Topic.category_id == Category.id)
        .where(UserTopicStrength.user_id == current_user.id)
    )
    rows = result.all()
    strengths = [
        TopicStrengthResponse(
            topic_id=uts.topic_id,
            topic_name=topic.name,
            category_id=category.id,
            category_slug=category.slug,
            category_name=category.name,
            score=uts.score,
            strength_label=uts.strength_label,
        )
        for uts, topic, category in rows
    ]
    return UserProfileWithStrengthsResponse(
        id=str(current_user.id),
        username=current_user.username,
        email=current_user.email,
        role=current_user.role.value if hasattr(current_user.role, "value") else str(current_user.role),
        is_verified=current_user.is_verified,
        experience_level=current_user.experience_level.value if current_user.experience_level and hasattr(current_user.experience_level, "value") else current_user.experience_level,
        target_role=current_user.target_role,
        avatar_url=current_user.avatar_url,
        streak_count=current_user.streak_count,
        assessment_completed_at=current_user.assessment_completed_at.isoformat() if current_user.assessment_completed_at else None,
        topic_strengths=strengths,
        created_at=current_user.created_at.isoformat(),
    )


@router.get("/me/suggestions")
async def get_my_suggestions(
    domain: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Personalized suggestions for a domain using LLM (Groq) based on user's topic strengths."""
    from app.services.groq_client import get_personalized_suggestions

    cat_result = await db.execute(select(Category).where(Category.slug == domain))
    cat = cat_result.scalar_one_or_none()
    if not cat:
        raise HTTPException(status_code=404, detail="Domain not found")

    strength_result = await db.execute(
        select(UserTopicStrength, Topic, Category)
        .join(Topic, UserTopicStrength.topic_id == Topic.id)
        .join(Category, Topic.category_id == Category.id)
        .where(UserTopicStrength.user_id == current_user.id)
    )
    topic_strengths = [
        {
            "topic_id": uts.topic_id,
            "topic_name": topic.name,
            "category_slug": category.slug,
            "score": uts.score,
            "strength_label": uts.strength_label,
        }
        for uts, topic, category in strength_result.all()
    ]

    suggestions = await get_personalized_suggestions(
        topic_strengths, domain, cat.name
    )
    if suggestions:
        return {"personalized": True, "data": suggestions}

    # Fallback: rule-based personalization from topic strengths (no LLM needed)
    from app.services.groq_client import build_rule_based_suggestions
    strengths_for_domain = [s for s in topic_strengths if s.get("category_slug") == domain]
    if strengths_for_domain:
        fallback = build_rule_based_suggestions(topic_strengths, domain, cat.name)
        return {"personalized": True, "data": fallback}

    return {
        "personalized": False,
        "data": {
            "summary": "Complete your onboarding assessment to get personalized suggestions for this domain.",
            "next_steps": [],
            "topics_to_study_first": [],
            "topics_to_skip_or_review_lightly": [],
        },
    }


@router.get("/me/domains/{slug}/preference", response_model=DomainPreferenceResponse | None)
async def get_domain_preference(
    slug: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get current user's time commitment (duration_weeks) for a domain. None if not set."""
    cat_result = await db.execute(select(Category).where(Category.slug == slug))
    cat = cat_result.scalar_one_or_none()
    if not cat:
        raise HTTPException(status_code=404, detail="Domain not found")
    result = await db.execute(
        select(UserDomainPreference).where(
            UserDomainPreference.user_id == current_user.id,
            UserDomainPreference.category_id == cat.id,
        )
    )
    pref = result.scalar_one_or_none()
    if not pref:
        return None
    return DomainPreferenceResponse(duration_weeks=pref.duration_weeks)


@router.put("/me/domains/{slug}/preference", response_model=DomainPreferenceResponse)
async def set_domain_preference(
    slug: str,
    data: DomainPreferenceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Set how many weeks the user can spend on this domain (creates or updates)."""
    cat_result = await db.execute(select(Category).where(Category.slug == slug))
    cat = cat_result.scalar_one_or_none()
    if not cat:
        raise HTTPException(status_code=404, detail="Domain not found")
    if data.duration_weeks < 1 or data.duration_weeks > 104:
        raise HTTPException(status_code=400, detail="duration_weeks must be between 1 and 104")
    result = await db.execute(
        select(UserDomainPreference).where(
            UserDomainPreference.user_id == current_user.id,
            UserDomainPreference.category_id == cat.id,
        )
    )
    pref = result.scalar_one_or_none()
    if pref:
        pref.duration_weeks = data.duration_weeks
    else:
        pref = UserDomainPreference(
            user_id=current_user.id,
            category_id=cat.id,
            duration_weeks=data.duration_weeks,
        )
        db.add(pref)
    await db.commit()
    await db.refresh(pref)
    return DomainPreferenceResponse(duration_weeks=pref.duration_weeks)


@router.get("/me/domains/{slug}/roadmap/weeks/{week_number}/expand")
async def expand_roadmap_week(
    slug: str,
    week_number: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """LLM-generated granular tasks and resources (YouTube, articles, books) for a roadmap week. Requires auth."""
    from app.models.roadmap import RoadmapItem
    from app.services.groq_client import expand_week_content, build_fallback_expand_week

    cat_result = await db.execute(select(Category).where(Category.slug == slug))
    cat = cat_result.scalar_one_or_none()
    if not cat:
        raise HTTPException(status_code=404, detail="Domain not found")

    rm_result = await db.execute(
        select(RoadmapItem)
        .where(RoadmapItem.category_id == cat.id, RoadmapItem.week_number == week_number)
        .order_by(RoadmapItem.order_index)
        .limit(1)
    )
    rm = rm_result.scalar_one_or_none()
    if not rm:
        raise HTTPException(status_code=404, detail="Week not found")

    strength_result = await db.execute(
        select(UserTopicStrength, Topic, Category)
        .join(Topic, UserTopicStrength.topic_id == Topic.id)
        .join(Category, Topic.category_id == Category.id)
        .where(UserTopicStrength.user_id == current_user.id, Category.slug == slug)
    )
    topic_strengths = [
        {"topic_name": t.name, "strength_label": uts.strength_label, "category_slug": c.slug}
        for uts, t, c in strength_result.all()
    ]

    pref_result = await db.execute(
        select(UserDomainPreference).where(
            UserDomainPreference.user_id == current_user.id,
            UserDomainPreference.category_id == cat.id,
        )
    )
    pref = pref_result.scalar_one_or_none()
    duration_weeks = pref.duration_weeks if pref else 10

    content = await expand_week_content(
        roadmap_title=rm.title,
        roadmap_description=rm.description,
        week_number=week_number,
        duration_weeks=duration_weeks,
        topic_strengths=topic_strengths,
        domain_name=cat.name,
    )
    if not content:
        content = build_fallback_expand_week(rm.title, rm.description)

    return {
        "roadmap_item": {
            "id": rm.id,
            "title": rm.title,
            "description": rm.description,
            "week_number": rm.week_number,
        },
        "granular_tasks": content.get("granular_tasks", []),
        "resources": content.get("resources", []),
    }


@router.get("/by-username/{username}", response_model=UserResponse)
async def get_user_by_username(username: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/{user_id}/profile", response_model=UserResponse)
async def get_user_profile(user_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}/profile", response_model=UserResponse)
async def update_profile(
    user_id: str,
    data: UserProfileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Cannot update another user's profile")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)

    await db.flush()
    await db.refresh(current_user)
    return current_user


@router.get("/{user_id}/submissions", response_model=list[SubmissionResponse])
async def get_user_submissions(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    limit: int = 50,
    offset: int = 0,
):
    result = await db.execute(
        select(Submission)
        .where(Submission.user_id == user_id)
        .order_by(Submission.submitted_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return result.scalars().all()


@router.get("/leaderboard")
async def get_leaderboard(db: AsyncSession = Depends(get_db), limit: int = 50):
    result = await db.execute(
        select(
            User.id,
            User.username,
            User.avatar_url,
            User.streak_count,
            func.count(Submission.id).label("total_submissions"),
        )
        .outerjoin(Submission, Submission.user_id == User.id)
        .group_by(User.id)
        .order_by(func.count(Submission.id).desc())
        .limit(limit)
    )
    rows = result.all()
    return [
        {
            "user_id": str(r.id),
            "username": r.username,
            "avatar_url": r.avatar_url,
            "streak_count": r.streak_count,
            "total_submissions": r.total_submissions,
        }
        for r in rows
    ]
