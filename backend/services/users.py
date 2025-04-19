from sqlalchemy.orm import Session
from ..models.users import User
from ..schemas.users import UserLogin, UserCreate
from .security import verify_password, create_access_token, hash_password
from fastapi import HTTPException, status
from ..models.enums import UserRole


def login_user(db: Session, credentials: UserLogin):
    """
    Authenticates a user using either their username or email and password.

    Args:
        db (Session): SQLAlchemy session for database interaction.
        credentials (UserLogin): Object containing the user's login (username or email) and password.

    Returns:
        str: A JWT access token if authentication is successful.

    Raises:
        HTTPException: Raised with status 401 if the login or password is incorrect.
    """

    if '@' in credentials.login:
        user = db.query(User).filter(User.email == credentials.login).first()
    else:
        user = db.query(User).filter(User.username == credentials.login).first()

    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login or password"
        )

    jwt_token = create_access_token(data={"sub": user.id})

    return jwt_token


def register_user(db: Session, credentials: UserCreate):
    """
    Registers a new user by storing their credentials in the database.

    Args:
        db (Session): SQLAlchemy session for database interaction.
        credentials (UserCreate): Object containing the user's email, username, and password.

    Returns:
        str: A JWT access token generated after successful registration.

    Raises:
        HTTPException:
            - 400 if the email is already registered.
            - 400 if the username is already taken.
    """

    check_email = db.query(User).filter(User.email == credentials.email).first()
    if check_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered"
        )

    check_username = db.query(User).filter(User.username == credentials.username).first()
    if check_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already taken"
        )

    new_user = User(
        email=credentials.email,
        username=credentials.username,
        password=hash_password(credentials.password),
        role=UserRole.user
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    jwt_token = create_access_token(data={"sub": new_user.id})

    return jwt_token
