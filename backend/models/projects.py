from datetime import datetime
from ..db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Text, DateTime, Boolean, Enum as SQLEnum, ForeignKey, Table, Column
from ..models.enums import ProjectRole

projects_owners = Table(
    """
    Association table linking projects with their owners, which can be either users or teams.
    
    This table allows a project to have multiple owners, including both individual users and entire teams.
    
    Columns:
        project_id (int): Foreign key referencing the ID of the project. Part of the composite primary key.
        user_id (int): Foreign key referencing the ID of the user. Part of the composite primary key. Can be null if the owner is a team.
        team_id (int): Foreign key referencing the ID of the team. Part of the composite primary key. Can be null if the owner is a user.
    
    Note:
        Either `user_id` or `team_id` should be non-null for a valid ownership record.
    """
    "projects_owners",
    Base.metadata,
    Column("project_id", ForeignKey("projects.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("team_id", ForeignKey("teams.id"), primary_key=True)
)


class Project(Base):
    """
    Represents a project in the system.

    Attributes:
        id (int): Unique identifier for the project.
        title (str): Title of the project (required).
        description (str): Detailed description of the project.
        created_at (datetime): Timestamp of when the project was created. Defaults to the current time.
        is_closed (bool): Indicates whether the project is closed. Defaults to False.

        owner_users (list[User]): List of users who are owners of the project.
        owner_teams (list[Team]): List of teams that own the project.
        project_roles (list[ProjectRole]): List of roles assigned to users within the project, defining their permissions (e.g., admin, contributor, watcher).
    """
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    description: Mapped[str] = mapped_column(
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

    owner_users: Mapped[list["User"]] = relationship(
        "User",
        secondary=projects_owners,
        back_populates="owned_projects",
        overlaps="owned_projects"
    )
    owner_teams: Mapped[list["Team"]] = relationship(
        "Team",
        secondary=projects_owners,
        back_populates="owned_projects",
        overlaps="owned_projects"
    )
    project_roles: Mapped[list["ProjectRole"]] = relationship(
        "ProjectRole",
        back_populates="project",
        overlaps="project"
    )


class ProjectRole(Base):
    """
    Represents the role of a user within a specific project.

    Attributes:
        user_id (int): Foreign key linking to the ID of the user. Part of the composite primary key.
        project_id (int): Foreign key linking to the ID of the project. Part of the composite primary key.
        role (ProjectRole): Enum value representing the user's role in the project (e.g., admin, contributor, watcher).

        project (Project): Relationship to the associated project.
        user (User): Relationship to the associated user.
    """
    __tablename__ = 'project_roles'

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        primary_key=True
    )
    project_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("projects.id"),
        primary_key=True
    )
    role: Mapped[ProjectRole] = mapped_column(
        SQLEnum(ProjectRole, name="project_role", create_type=False),
        default=ProjectRole.watcher
    )

    project: Mapped[Project] = relationship(
        "Project",
        back_populates="project_roles"
    )
    user: Mapped[["User"]] = relationship(
        "User",
        back_populates="project_roles",
    )
