from sqlalchemy import String, Integer, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

import enum


class DifficultyLevel(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    VERY_HARD = "very_hard"
    CASE_STUDY = "case_study"


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    name: Mapped[str] = mapped_column(String(100))
    difficulty_level: Mapped[str] = mapped_column(
        SAEnum(DifficultyLevel, name="difficulty_level"), default=DifficultyLevel.EASY
    )
    order_index: Mapped[int] = mapped_column(Integer, default=0)

    category = relationship("Category", back_populates="topics")
    questions = relationship("Question", back_populates="topic")
    assessment_questions = relationship("AssessmentQuestion", back_populates="topic")
    user_strengths = relationship("UserTopicStrength", back_populates="topic")
