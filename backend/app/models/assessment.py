import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Integer, Float, ForeignKey, Text, DateTime, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

import enum


class QuestionType(str, enum.Enum):
    MCQ = "mcq"
    SCALE = "scale"  # 1-5 self-rating


class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    question_text: Mapped[str] = mapped_column(Text)
    question_type: Mapped[str] = mapped_column(SAEnum(QuestionType, name="assessment_question_type"))
    options: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # for MCQ: {"a": "Never", "b": "Sometimes", ...}
    scale_max: Mapped[int | None] = mapped_column(Integer, nullable=True)  # for scale: 5
    order_index: Mapped[int] = mapped_column(Integer, default=0)

    topic = relationship("Topic", back_populates="assessment_questions")
    category = relationship("Category")


class UserAssessmentAnswer(Base):
    __tablename__ = "user_assessment_answers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    question_id: Mapped[int] = mapped_column(ForeignKey("assessment_questions.id"))
    answer_value: Mapped[str] = mapped_column(String(100))  # option key or "3" for scale
    score: Mapped[float] = mapped_column(Float, default=0.0)  # 0-100 normalized
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("User", back_populates="assessment_answers")
    question = relationship("AssessmentQuestion")


class UserTopicStrength(Base):
    __tablename__ = "user_topic_strengths"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    score: Mapped[float] = mapped_column(Float, default=0.0)  # 0-100
    strength_label: Mapped[str] = mapped_column(String(20), default="beginner")  # beginner | intermediate | advanced
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user = relationship("User", back_populates="topic_strengths")
    topic = relationship("Topic", back_populates="user_strengths")
