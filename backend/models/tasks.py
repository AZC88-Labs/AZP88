from datetime import datetime
from ..db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Text, DateTime


class Task(Base):
    """
    TODO:docs
    """
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    project_id: Mapped[int] = mapped_column(
        Integer
    )

    title: Mapped[String] = mapped_column(
        String(255)
    )

    description: Mapped[String] = mapped_column(
        Text
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )

    # TODO:relationships and db rework

