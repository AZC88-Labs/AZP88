from datetime import datetime
from ..db import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import String, Enum as SQLEnum, Text, Integer, DateTime, ForeignKey
from .enums import TeamRole
from .projects import projects_owners

class Team(Base):
    """
    Represents a team in the database.

    Attributes:
        id (int): Unique identifier for the team.
        name (str): Name of the team (must be unique).
        description (str): Description of the team's purpose.
        created_at (datetime): Timestamp when the team was created.

        users (list[User]): List of users associated with the team, linked via the 'team_members' association table.
        team_members (list[TeamMember]): List of TeamMember objects, representing users and their roles within the team.
        owned_projects (list[Project]): Projects owned by this team, linked via the 'projects_owners' table.
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
        Text
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )

    users: Mapped[list["User"]] = relationship(
        "User",
        secondary="team_members",
        back_populates="teams",
        overlaps="team_members,user,team"
    )
    team_members: Mapped[list["TeamMember"]] = relationship(
        "TeamMember",
        back_populates="team",
        overlaps="teams,users,user"
    )
    owned_projects: Mapped[list["Project"]] = relationship(
        "Project",
        secondary=projects_owners,
        back_populates="owner_teams",
        overlaps="owner_teams"
    )


class TeamMember(Base):
    """
    Represents the association between a user and a team, along with the user's role in the team.

    Attributes:
        user_id (int): Foreign key referencing the user's ID.
        group_id (int): Foreign key referencing the team's ID.
        role (TeamRole): User's role in the team, defined by the TeamRole enumeration (admin, member, guest, or pending).

        team (Team): Relationship to the Team model, linking the user to the team.
        user (User): Relationship to the User model, linking the user to their team membership.
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
        back_populates="team_members",
        overlaps="teams,users"
    )
    team: Mapped["Team"] = relationship(
        "Team",
        back_populates="team_members",
        overlaps="teams,users"
    )
