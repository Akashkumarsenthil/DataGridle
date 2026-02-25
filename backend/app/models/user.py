import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Boolean, Integer, DateTime, Enum as SAEnum, Text
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

import enum


class UserRole(str, enum.Enum):
    USER = "user"
    CREATOR = "creator"
    ADMIN = "admin"
    MODERATOR = "moderator"


class ExperienceLevel(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(SAEnum(UserRole, name="user_role"), default=UserRole.USER)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    experience_level: Mapped[str | None] = mapped_column(
        SAEnum(ExperienceLevel, name="experience_level"), nullable=True
    )
    target_role: Mapped[str | None] = mapped_column(String(100), nullable=True)
    target_companies: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    streak_count: Mapped[int] = mapped_column(Integer, default=0)
    assessment_completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    submissions = relationship("Submission", back_populates="user")
    discussions = relationship("Discussion", back_populates="author")
    progress = relationship("UserProgress", back_populates="user")
    badges = relationship("UserBadge", back_populates="user")
    assessment_answers = relationship("UserAssessmentAnswer", back_populates="user")
    topic_strengths = relationship("UserTopicStrength", back_populates="user")
    domain_preferences = relationship("UserDomainPreference", back_populates="user")
