import re
from pydantic import BaseModel, field_validator
from ..models.enums import UserRole
from argon2 import PasswordHasher

pwd_hash = PasswordHasher()


class UserBase(BaseModel):
    username: str
    email: str
    role: UserRole


class UserCreate(UserBase):
    password: str

    @field_validator('password')
    def validate_password(cls, password: str) -> str:
        """
        Checks if password length is long enough and not too long.
        Password also must contain at least one special character.

        :param password: plain text password to verify
        :return: hashed password to verify or ValueError.
        """
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters')
        if len(password) > 50:
            raise ValueError('Password must be at most 50 characters')
        if not re.search(r'[\W_]', password):
            raise ValueError('Password must contain at least one special character')
        if not re.search(r'[A-Z]', password):
            raise ValueError('Password must contain at least one uppercase letter')
        return pwd_hash.hash(password)

    @field_validator('email')
    def validate_email(cls, email: str) -> str:
        """
        Checks if email contains '@' and is of sufficient length.

        :param email: plain text email to verify
        :return: ValueError or plain text email.
        """
        if '@' not in email:
            raise ValueError('Email must contain "@"')
        if len(email) < 5:
            raise ValueError('Email is too short, must be at least 5 characters')
        return email
