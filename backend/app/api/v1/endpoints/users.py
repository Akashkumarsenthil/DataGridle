from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.submission import Submission
from app.models.progress import UserProgress
from app.models.badge import UserBadge, Badge
from app.schemas.user import UserResponse, UserProfileUpdate
from app.schemas.question import SubmissionResponse

router = APIRouter(prefix="/users", tags=["Users"])


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
