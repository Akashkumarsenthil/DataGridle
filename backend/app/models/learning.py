import uuid

from sqlalchemy import String, Integer, ForeignKey, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

import enum


class ResourceType(str, enum.Enum):
    VIDEO = "video"
    ARTICLE = "article"
    PLAYLIST = "playlist"


class LearningResource(Base):
    __tablename__ = "learning_resources"

    id: Mapped[int] = mapped_column(primary_key=True)
    topic_id: Mapped[int | None] = mapped_column(ForeignKey("topics.id"), nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    roadmap_item_id: Mapped[int | None] = mapped_column(ForeignKey("roadmap_items.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(300))
    url: Mapped[str] = mapped_column(String(500))
    resource_type: Mapped[str] = mapped_column(SAEnum(ResourceType, name="resource_type"))
    difficulty_level: Mapped[str | None] = mapped_column(String(20), nullable=True)
    estimated_duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    order_in_playlist: Mapped[int] = mapped_column(Integer, default=0)
    added_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    roadmap_item = relationship("RoadmapItem", back_populates="resources")
