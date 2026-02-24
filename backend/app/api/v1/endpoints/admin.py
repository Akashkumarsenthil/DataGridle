from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.models.question import Question, QuestionStatus
from app.schemas.user import UserResponse
from app.schemas.question import QuestionResponse

router = APIRouter(prefix="/admin", tags=["Admin"])


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@router.get("/pending-creators", response_model=list[UserResponse])
async def get_pending_creators(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    result = await db.execute(
        select(User).where(User.role == UserRole.CREATOR, User.is_verified == False)
    )
    return result.scalars().all()


@router.post("/approve-creator/{user_id}", response_model=UserResponse)
async def approve_creator(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_verified = True
    return user


@router.get("/pending-questions", response_model=list[QuestionResponse])
async def get_pending_questions(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    result = await db.execute(
        select(Question).where(Question.status == QuestionStatus.PENDING)
    )
    return result.scalars().all()


@router.post("/approve-question/{question_id}", response_model=QuestionResponse)
async def approve_question(
    question_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    result = await db.execute(select(Question).where(Question.id == question_id))
    question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    question.status = QuestionStatus.APPROVED
    return question


@router.post("/reject-question/{question_id}", response_model=QuestionResponse)
async def reject_question(
    question_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    result = await db.execute(select(Question).where(Question.id == question_id))
    question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    question.status = QuestionStatus.REJECTED
    return question


@router.get("/analytics")
async def get_analytics(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    users_count = await db.execute(select(func.count(User.id)))
    questions_count = await db.execute(select(func.count(Question.id)))
    return {
        "total_users": users_count.scalar(),
        "total_questions": questions_count.scalar(),
    }
