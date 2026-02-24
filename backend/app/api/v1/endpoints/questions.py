from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.question import Question, QuestionStatus
from app.models.submission import Submission, SubmissionResult
from app.schemas.question import (
    QuestionCreate,
    QuestionUpdate,
    QuestionResponse,
    QuestionDetailResponse,
    SubmissionCreate,
    SubmissionResponse,
)

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.get("/", response_model=list[QuestionResponse])
async def list_questions(
    db: AsyncSession = Depends(get_db),
    category_id: int | None = None,
    topic_id: int | None = None,
    difficulty: str | None = None,
    question_type: str | None = None,
    limit: int = Query(default=50, le=100),
    offset: int = 0,
):
    query = select(Question).where(Question.status == QuestionStatus.APPROVED)

    if category_id:
        query = query.where(Question.category_id == category_id)
    if topic_id:
        query = query.where(Question.topic_id == topic_id)
    if difficulty:
        query = query.where(Question.difficulty == difficulty)
    if question_type:
        query = query.where(Question.question_type == question_type)

    query = query.order_by(Question.created_at.desc()).limit(limit).offset(offset)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{question_id}", response_model=QuestionDetailResponse)
async def get_question(question_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Question).where(Question.id == question_id))
    question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.post("/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(
    data: QuestionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role not in ("creator", "admin"):
        raise HTTPException(status_code=403, detail="Only creators and admins can create questions")

    question = Question(
        **data.model_dump(exclude={"company_ids"}),
        creator_id=current_user.id,
    )
    db.add(question)
    await db.flush()
    await db.refresh(question)
    return question


@router.put("/{question_id}", response_model=QuestionResponse)
async def update_question(
    question_id: int,
    data: QuestionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Question).where(Question.id == question_id))
    question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    if current_user.role != "admin" and question.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this question")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(question, field, value)

    await db.flush()
    await db.refresh(question)
    return question


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(
    question_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete questions")

    result = await db.execute(select(Question).where(Question.id == question_id))
    question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    await db.delete(question)


@router.post("/{question_id}/submit", response_model=SubmissionResponse)
async def submit_answer(
    question_id: int,
    data: SubmissionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Question).where(Question.id == question_id))
    question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # For MVP, basic comparison — real evaluation happens client-side via DuckDB-WASM
    submission = Submission(
        user_id=current_user.id,
        question_id=question_id,
        submitted_code=data.submitted_code,
        language=data.language,
        result=SubmissionResult.PASS,
    )
    db.add(submission)
    await db.flush()
    await db.refresh(submission)
    return submission
