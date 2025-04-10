from datetime import datetime
from ..db import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import String, Enum as SQLEnum, Text, Integer, DateTime, ForeignKey
from .enums import TeamRole


class Team(Base):
    __tablename__ = 'teams'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    users: Mapped[list["User"]] = relationship("User", secondary="team_members", back_populates="groups")
    group_members: Mapped[list["TeamMember"]] = relationship("TeamMember", back_populates="group")


class TeamMember(Base):
    __tablename__ = 'team_members'

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey('teams.id'), primary_key=True)
    role: Mapped[TeamRole] = mapped_column(SQLEnum(TeamRole, name="team_role", create_type=False),
                                           default=TeamRole.member)

    user: Mapped["User"] = relationship("User", back_populates="group_members")
    group: Mapped["Team"] = relationship("Team", back_populates="group_members")
