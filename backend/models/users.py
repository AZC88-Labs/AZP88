from .groups import GroupMember, Group
from ..db import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import String, Enum, Integer
from .enums import UserRole
from ..dependencies import hash_password, verify_password


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role", create_type=False), default=UserRole.user)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    groups: Mapped[list[Group]] = relationship("Group", secondary="group_members", back_populates="users")
    group_members: Mapped[list[GroupMember]] = relationship("GroupMember", back_populates="user")

    def __init__(self, username: str, password: str):
        self.username = username
        self.hashed_password = hash_password(password)

    def check_password(self, password: str) -> bool:
        """
        Checks if password matches hashed password.

        :param password: plain text password to verify
        :type password: str
        :return: True if the password matches, otherwise False
        :rtype: bool
        """
        return verify_password(password, self.hashed_password)
