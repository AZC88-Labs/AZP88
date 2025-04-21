import re
from pydantic import BaseModel, field_validator, EmailStr


class UserBase(BaseModel):
    """
    Basic User's pydantic schema.
    """

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    """
    Pydantic model for creating new users.

    This class extends `UserBase` and adds fields required for user creation, such as:
    - `password`: The password for the user.
    - `email`: The user's email address.
    - `username`: The user's chosen username.

    Attributes:
        password (str): The password for the new user.
        email (str): The email address of the new user.
        username (str): The chosen username for the new user.

    This model is used for validating incoming data when creating a new user in the system.
    """

    password: str
    email: str
    username: str

    @field_validator('password')
    def validate_password(cls, password: str) -> str:
        """
        Validate the password for the new user.

        This method checks whether the provided password fulfills the following requirements:
            - Length between 8 and 255 characters.
            - Contains at least one special character from the set: `!@#$%^&*`.
            - Contains at least one uppercase letter.
            - Contains at least one digit.
            - Contains no whitespace characters (e.g., space, tab).
            - Does not contain prohibited characters: ' " \ / < > ( ) { } [ ] ;.

        Args:
            password (str): The password for the new user.

        Returns:
            str: The valid password if all requirements are met.

        Raises:
            ValueError: If the password does not meet any of the validation criteria.
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
        Validate the email for the new user.

        This method checks whether the provided email fulfills the following requirements:
            - Length between 5 and 254 characters.
            - Has a valid email structure: example@example_domain.com

        Args:
            email (str): The email for the new user.

        Returns:
            str: The valid email if all requirements are met.

        Raises:
            ValueError: If the email does not meet any of the validation criteria.
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
        Validate the username for the new user.

        This method checks whether the provided username fulfills the following requirements:
            - Length between 5 and 30 characters.
            - Contains only letters, numbers, hyphens and underscores.

        Args:
            username (str): The username for the new user.

        Returns:
            str: The valid username if all requirements are met.

        Raises:
            ValueError: If the username does not meet any of the validation criteria.
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
    Pydantic model for authentication the user.

    This class extends `UserBase` and adds fields required for user login, such as:
    - `password`: The password for the user.
    - `login`: The user's login or email address.

    Attributes:
        login (str): The user's login or email address.
        password (str): The password for the user.

    This model is used for validating incoming data when authenticating a user in the system.
    """
    login: str
    password: str

    @field_validator('password')
    def validate_password_not_empty(cls, password: str) -> str:
        """
        Validates that the password is not empty or only whitespace.

        Args:
            password (str): The password provided by the user during login.

        Returns:
            str: The validated password.

        Raises:
            ValueError: If the password is empty or contains only whitespace.
        """

        if not password.strip():
            raise ValueError("Password cannot be empty")
        return password

    @field_validator('login')
    def validate_login(cls, login: str) -> str:
        """
        Validates the login field by ensuring it is not empty, stripping whitespace,
        and verifying email format if applicable.

        If the login input appears to be an email address, it is converted to lowercase
        and validated using Pydantic's `EmailStr` validator.

        Args:
            login (str): The login identifier provided by the user, which can be a username or email address.

        Returns:
            str: The cleaned and validated login string.

        Raises:
            ValueError: If the login is empty or resembles an email address but is not in a valid format.
        """

        login = login.strip()

        if not login:
            raise ValueError("Login cannot be empty")

        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', login):
            login = login.lower()

            try:
                EmailStr.validate(login)
            except ValueError:
                raise ValueError("Invalid e-mail address")

        return login
