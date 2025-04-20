from datetime import datetime
from ..db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Text, DateTime, Boolean, Enum as SQLEnum
from ..models.enums import ProjectRole, TeamRole


class Project(Base):
    """
    TODO:docs
    """

    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    title: Mapped[String] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[String] = mapped_column(
        Text
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        default=datetime.now
    )

    is_closed: Mapped[Boolean] = mapped_column(
        Boolean,
        default=False
    )

    # TODO:relationships


class ProjectRole(Base):
    """
    TODO:docs
    """

    __tablename__ = 'project_roles'

    user_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    project_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    role: Mapped[ProjectRole] = mapped_column(
        SQLEnum(ProjectRole, name="project_role", create_type=False),
        default=ProjectRole.watcher
    )

#     TODO: relationships

class ProjectOwner(Base):
    """
    TODO:docs
    """

    __tablename__ = 'project_owners'

    user_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    team_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    project_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    # TODO:relationships and db rework.