"""User's time commitment per domain (for dynamic roadmap pacing)."""

import uuid

from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class UserDomainPreference(Base):
    """How many weeks/months the user can spend on a domain (one row per user per category)."""

    __tablename__ = "user_domain_preferences"
    __table_args__ = (UniqueConstraint("user_id", "category_id", name="uq_user_category"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    duration_weeks: Mapped[int] = mapped_column(Integer, nullable=False, default=10)

    user = relationship("User", back_populates="domain_preferences")
    category = relationship("Category", back_populates="domain_preferences")
