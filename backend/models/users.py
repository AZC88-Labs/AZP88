from .teams import Team, TeamMember
from ..db import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import String, Enum, Integer
from .enums import UserRole


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role", create_type=False), default=UserRole.user)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    groups: Mapped[list[Team]] = relationship("Team", secondary="team_members", back_populates="users")
    group_members: Mapped[list[TeamMember]] = relationship("TeamMember", back_populates="user")
