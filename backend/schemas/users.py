import re
from pydantic import BaseModel, field_validator, EmailStr
from ..services.security import hash_password


class UserBase(BaseModel):
    """
    Basic User's pydantic schema.
    """

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    """
    TODO
    """
    password: str
    email: str
    username: str

    @field_validator('password')
    def validate_password(cls, password: str) -> str:
        """
        TODO
        """
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if len(password) > 255:
            raise ValueError("Password must be at most 255 characters long.")

        if not re.search(r"[!@#$%^&*]", password):
            raise ValueError("Password must contain at least one special character (!@#$%^&*).")

        if not re.search(r"[A-Z]", password):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"[0-9]", password):
            raise ValueError("Password must contain at least one digit.")

        if re.search(r"\s", password):
            raise ValueError("Whitespace characters (e.g., space, tab) are not allowed.")

        if re.search(r"[\'\"\\/<>(){}\[\];`]", password):
            raise ValueError("Password contains prohibited special characters.")

        return password

    @field_validator('email')
    def validate_email(cls, email: str) -> str:
        """
        TODO
        """
        email = email.lower().strip()

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
        TODO
        """
        username = username.strip()

        if len(username) < 5:
            raise ValueError('Username must contain at least 5 characters')
        if len(username) > 30:
            raise ValueError('Username is too long, must be at most 30 characters')
        if not re.fullmatch(r'^[a-zA-Z0-9][a-zA-Z0-9_-]*$', username):
            raise ValueError(
                "Username must start with a letter or a number and may only contain letters, numbers, underscores (_) or hyphens (-).")
        return username


class UserLogin(UserBase):
    """
    TODO
    """
    login: str
    password: str

    @field_validator('password')
    def validate_password_not_empty(cls, value: str) -> str:
        """
        TODO
        """
        if not value.strip():
            raise ValueError("Password cannot be empty")
        return value

    @field_validator('login')
    def validate_login(cls, login: str) -> str:
        """
        TODO
        """
        login = login.strip()

        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', login):
            login = login.lower()

            try:
                EmailStr.validate(login)
            except ValueError:
                raise ValueError("Invalid e-mail address")
            return login
        else:
            return login
