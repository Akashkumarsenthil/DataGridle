from datetime import date

from sqlalchemy import Integer, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class DailyQuestion(Base):
    __tablename__ = "daily_questions"
    __table_args__ = (UniqueConstraint("category_id", "date", name="uq_daily_category_date"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    date: Mapped[date] = mapped_column(Date)

    question = relationship("Question")
