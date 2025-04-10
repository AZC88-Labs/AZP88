import re
from pydantic import BaseModel, field_validator
from ..models.enums import UserRole
from ..services.security import hash_password


class UserBase(BaseModel):
    username: str
    email: str
    role: UserRole

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str

    @field_validator('password')
    def validate_password(cls, password: str) -> str:
        """
        Checks if password length is valid.
        Requirements:
        len: (8;50);
        at least one special character;
        at least one uppercase letter and one digit.
        It is prohibited to use whitespaces or dangerous special characters.

        :param password: plain text password to verify
        :return: hashed password to verify or ValueError.
        :raises ValueError: If any of the validation conditions are not met.
        """
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters')
        if len(password) > 50:
            raise ValueError('Password must be at most 50 characters')
        if not re.search(r'[!_-]', password):
            raise ValueError('Password must contain at least one special character (!, _ or -)')
        if not re.search(r'[A-Z]', password) or not re.search(r'[0-9]', password):
            raise ValueError("Password must contain at least one uppercase letter and one digit")
        if re.search(r'\s', password):
            raise ValueError("It is prohibited to use space or other whitespace")
        if re.search(r'[%^&#@<>\'";/\\(){}\[\]]', password):
            raise ValueError("You used prohibited special sign")
        return hash_password(password)

    @field_validator('email')
    def validate_email(cls, email: str) -> str:
        """
        Checks if email contains '@' and domain. It also checks length of the email.

        :param email: plain text email to verify
        :return: ValueError or plain text email.
        :raises ValueError: If any of the validation conditions are not met.
        """
        if len(email) < 5:
            raise ValueError('Email is too short, must be at least 5 characters')
        if len(email) > 254:
            raise ValueError('Email is too long, must be at most 254 characters')
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError("Invalid email structure. Must contain '@' and domain.")
        return email

    @field_validator('username')
    def validate_username(cls, username: str) -> str:
        """
        Validates the username based on the following criteria:
        - Length must be between 5 and 254 characters.
        - It must not contain spaces or any other whitespace characters.
        - It must not contain prohibited special characters.

        :param username: The username to be validated.
        :return: The valid username if all conditions are met.
        :raises ValueError: If any of the validation conditions are not met.
        """
        if len(username) < 5:
            raise ValueError('Username must contain at least 5 characters')
        if len(username) > 254:
            raise ValueError('Username is too long, must be at most 254 characters')
        if re.search(r'\s', username):
            raise ValueError("It is prohibited to use space or other whitespace")
        if re.search(r'[%^&#@<>\'";/\\(){}\[\]]', username):
            raise ValueError("You used prohibited special sign")
        return username


class UserLogin(UserBase):
    password: str

    @field_validator('email')
    def validate_email(cls, email: str) -> str:
        """
        Checks if email contains '@' and domain. It also checks length of the email.

        :param email: plain text email to verify
        :return: ValueError or plain text email.
        :raises ValueError: If any of the validation conditions are not met.
        """
        if len(email) < 5:
            raise ValueError('Email is too short, must be at least 5 characters')
        if len(email) > 254:
            raise ValueError('Email is too long, must be at most 254 characters')
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError("Invalid email structure. Must contain '@' and domain.")
        return email
