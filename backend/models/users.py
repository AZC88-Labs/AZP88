from ..db import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import String, Enum, Integer
from .enums import UserRole
from .teams import Team, TeamMember


class User(Base):
    """
    Represents a user in the database.

    Attributes:
        id (int): Unique identifier for the user.
        username (str): Unique username for the user.
        email (str): Email address of the user (must be unique).
        role (UserRole): User's role in the system, defined by the UserRole enumeration (admin, user). Default value is 'user'.
        password (str): User's hashed password stored in the database.
        groups (list[Team]): List of teams the user belongs to, through the 'team_members' table.
        group_members (list[TeamMember]): List of TeamMember objects representing the user's membership in teams.
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

    groups: Mapped[list["Team"]] = relationship(
        "Team",
        secondary="team_members",
        back_populates="users",
        overlaps="group_members,user,group"
    )
    group_members: Mapped[list["TeamMember"]] = relationship(
        "TeamMember",
        back_populates="user",
        overlaps="groups,users,group"
    )
