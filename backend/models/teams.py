from datetime import datetime
from ..db import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import String, Enum as SQLEnum, Text, Integer, DateTime, ForeignKey
from .enums import TeamRole


class Team(Base):
    """
    Represents a team in the database.

    Attributes:
        id (int): Unique identifier for the team.
        name (str): Name of the team (must be unique).
        description (str): Description of the team's purpose.
        created_at (datetime): Timestamp when the team was created.
        users (list[User]): List of users associated with the team through the 'team_members' table.
        group_members (list[TeamMember]): List of TeamMember objects representing the team's members and roles.
    """
    __tablename__ = 'teams'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )

    users: Mapped[list["User"]] = relationship(
        "User",
        secondary="team_members",
        back_populates="groups",
        overlaps="group_members,user,group"
    )
    group_members: Mapped[list["TeamMember"]] = relationship(
        "TeamMember",
        back_populates="group",
        overlaps="groups,users,user"
    )


class TeamMember(Base):
    """
    Association table linking users to teams.

    Stores the user's role within a specific team.

    Attributes:
        user_id (int): Foreign key referencing the user's ID.
        group_id (int): Foreign key referencing the team's ID.
        role (TeamRole): User's role in the team, defined by the TeamRole enumeration
            (admin, member, guest, or pending — waiting to be accepted).
        group (Team): Relationship to the Team model.
    """
    __tablename__ = 'team_members'

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('users.id'),
        primary_key=True
    )
    group_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('teams.id'),
        primary_key=True
    )
    role: Mapped[TeamRole] = mapped_column(
        SQLEnum(TeamRole, name="team_role", create_type=False),
        default=TeamRole.member
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="group_members",
        overlaps="groups,users"
    )
    group: Mapped["Team"] = relationship(
        "Team",
        back_populates="group_members",
        overlaps="groups,users"
    )
