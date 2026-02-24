import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    String, Integer, Text, ForeignKey, DateTime,
    Enum as SAEnum,
)
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

import enum


class QuestionType(str, enum.Enum):
    SQL = "sql"
    PYTHON = "python"
    MCQ = "mcq"
    CASE_STUDY = "case_study"


class QuestionDifficulty(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class QuestionStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ValidityMarker(str, enum.Enum):
    CURRENT = "current"
    OUTDATED = "outdated"


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    creator_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(300))
    description: Mapped[str] = mapped_column(Text)
    question_type: Mapped[str] = mapped_column(SAEnum(QuestionType, name="question_type"))
    difficulty: Mapped[str] = mapped_column(SAEnum(QuestionDifficulty, name="question_difficulty"))
    starter_code: Mapped[str | None] = mapped_column(Text, nullable=True)
    test_cases: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    expected_output: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    solution: Mapped[str | None] = mapped_column(Text, nullable=True)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    dataset_id: Mapped[int | None] = mapped_column(ForeignKey("datasets.id"), nullable=True)
    status: Mapped[str] = mapped_column(
        SAEnum(QuestionStatus, name="question_status"), default=QuestionStatus.PENDING
    )
    interview_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    validity_marker: Mapped[str] = mapped_column(
        SAEnum(ValidityMarker, name="validity_marker"), default=ValidityMarker.CURRENT
    )
    frequency_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    topic = relationship("Topic", back_populates="questions")
    creator = relationship("User")
    submissions = relationship("Submission", back_populates="question")
    company_tags = relationship("QuestionCompanyMap", back_populates="question")


class QuestionCompanyMap(Base):
    __tablename__ = "question_company_map"

    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    company_id: Mapped[int] = mapped_column(ForeignKey("company_tags.id"))
    role_asked_for: Mapped[str | None] = mapped_column(String(100), nullable=True)
    interview_round: Mapped[str | None] = mapped_column(String(100), nullable=True)
    reported_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )

    question = relationship("Question", back_populates="company_tags")
    company = relationship("CompanyTag")
