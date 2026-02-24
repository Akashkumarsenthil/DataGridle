from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class RoadmapItem(Base):
    __tablename__ = "roadmap_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    week_number: Mapped[int] = mapped_column(Integer, default=1)
    estimated_hours: Mapped[int] = mapped_column(Integer, default=3)

    category = relationship("Category", back_populates="roadmap_items")
    resources = relationship("LearningResource", back_populates="roadmap_item")
