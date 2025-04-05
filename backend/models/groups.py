from datetime import datetime
from ..db import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import String, Enum, Text, Integer, DateTime, ForeignKey
from enums import GroupRole
from users import User


class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    users: Mapped[list[User]] = relationship("User", secondary="group_members", back_populates="groups")
    group_members: Mapped[list["GroupMember"]] = relationship("GroupMember", back_populates="group")


class GroupMember(Base):
    __tablename__ = 'group_members'

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey('groups.id'), primary_key=True)
    role: Mapped[GroupRole] = mapped_column(Enum(GroupRole, name="group_role", create_type=False),
                                            default=GroupRole.member)

    user: Mapped[User] = relationship("User", back_populates="group_members")
    group: Mapped[Group] = relationship("Group", back_populates="group_members")
