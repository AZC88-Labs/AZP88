from ..db import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import String, Enum, Integer
from .enums import UserRole
from .teams import Team, TeamMember
from .projects import projects_owners

class User(Base):
    """
    Represents a user in the database.

    Attributes:
        id (int): Unique identifier for the user.
        username (str): Unique username for the user.
        email (str): Email address of the user (must be unique).
        role (UserRole): User's role in the system, defined by the UserRole enumeration (admin, user). Default value is 'user'.
        password (str): User's hashed password stored in the database.

        teams (list[Team]): List of teams the user belongs to, through the 'team_members' table.
        team_members (list[TeamMember]): List of TeamMember objects representing the user's membership in teams.
        owned_projects (list[Project]): List of Project objects where the user is one of the owners.
        task_assignees (list[TaskAssignee]): List of TaskAssignee objects, representing tasks assigned to the user, including role and assignment date.
        tasks_assigned (list[Task]): List of Task objects that the user is assigned to — convenience access via 'task_assignees'.
    """
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    username: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(
            UserRole,
            name="user_role",
            create_type=False
        ),
        default=UserRole.user
    )
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    teams: Mapped[list["Team"]] = relationship(
        "Team",
        secondary="team_members",
        back_populates="users",
        overlaps="team_members,user,team"
    )
    team_members: Mapped[list["TeamMember"]] = relationship(
        "TeamMember",
        back_populates="user",
        overlaps="teams,users,team"
    )
    owned_projects: Mapped[list["Project"]] = relationship(
        "Project",
        secondary=projects_owners,
        back_populates="owner_users",
        overlaps="owner_users"
    )
    task_assignees: Mapped[list["TaskAssignee"]] = relationship(
        "TaskAssignee",
        back_populates="user",
        overlaps="task"
    )
    tasks_assigned: Mapped[list["Task"]] = relationship(
        "Task",
        secondary="task_assignees",
        overlaps="task,task_assignees",
    )