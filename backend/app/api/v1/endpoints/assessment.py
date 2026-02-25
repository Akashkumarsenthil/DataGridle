from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.assessment import AssessmentQuestion, UserAssessmentAnswer, UserTopicStrength
from app.models.topic import Topic
from app.models.category import Category
from app.schemas.assessment import (
    AssessmentQuestionResponse,
    AssessmentSubmitRequest,
    TopicStrengthResponse,
)

router = APIRouter(prefix="/assessment", tags=["Assessment"])

MCQ_SCORE_MAP = {"a": 0, "b": 25, "c": 50, "d": 75, "e": 100}


def score_answer(question: AssessmentQuestion, answer_value: str) -> float:
    if question.question_type == "scale" and question.scale_max:
        try:
            v = float(answer_value)
            return min(100.0, max(0.0, (v / question.scale_max) * 100.0))
        except ValueError:
            return 0.0
    if question.question_type == "mcq" and answer_value.lower() in MCQ_SCORE_MAP:
        return float(MCQ_SCORE_MAP[answer_value.lower()])
    return 0.0


def strength_label(score: float) -> str:
    if score >= 67:
        return "advanced"
    if score >= 34:
        return "intermediate"
    return "beginner"


@router.get("/questions", response_model=list[AssessmentQuestionResponse])
async def list_questions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(AssessmentQuestion).order_by(AssessmentQuestion.order_index)
    )
    return result.scalars().all()


@router.post("/submit")
async def submit_assessment(
    body: AssessmentSubmitRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.assessment_completed_at:
        return {"message": "Assessment already completed", "already_completed": True}

    question_ids = [a.question_id for a in body.answers]
    result = await db.execute(
        select(AssessmentQuestion).where(AssessmentQuestion.id.in_(question_ids))
    )
    questions = {q.id: q for q in result.scalars().all()}

    topic_scores: dict[int, list[float]] = {}
    for a in body.answers:
        q = questions.get(a.question_id)
        if not q:
            continue
        score = score_answer(q, a.answer_value)
        uaa = UserAssessmentAnswer(
            user_id=current_user.id,
            question_id=q.id,
            answer_value=a.answer_value,
            score=score,
        )
        db.add(uaa)
        topic_scores.setdefault(q.topic_id, []).append(score)

    await db.flush()

    for topic_id, scores in topic_scores.items():
        avg = sum(scores) / len(scores) if scores else 0.0
        existing = await db.execute(
            select(UserTopicStrength).where(
                UserTopicStrength.user_id == current_user.id,
                UserTopicStrength.topic_id == topic_id,
            )
        )
        uts = existing.scalar_one_or_none()
        if uts:
            uts.score = avg
            uts.strength_label = strength_label(avg)
        else:
            uts = UserTopicStrength(
                user_id=current_user.id,
                topic_id=topic_id,
                score=avg,
                strength_label=strength_label(avg),
            )
            db.add(uts)

    current_user.assessment_completed_at = datetime.now(timezone.utc)
    await db.commit()
    return {"message": "Assessment submitted", "already_completed": False}
