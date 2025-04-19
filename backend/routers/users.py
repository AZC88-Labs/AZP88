from requests import Session
from ..dependencies import get_current_user
from ..models.users import User
from ..services.users import login_user, register_user
from fastapi import Depends, APIRouter
from ..db import get_db
from ..schemas.users import UserLogin, UserCreate, UserBase

router = APIRouter()


@router.post(
    "/login",
    summary="Authenticate user",
    description="Logs in a user using email and password, and returns a JWT access token.",
    tags=["Authentication"]
)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticates a user and returns a JWT access token.

    Args:
        user_data (UserLogin): The user's login credentials, validated via a Pydantic schema.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: A dictionary containing the JWT access token and token type.
    """

    jwt_token = login_user(db, user_data)

    return {"access_token": jwt_token, "token_type": "bearer"}


@router.put(
    "/register",
    summary="Register a new user",
    description="Creates a new user account and returns a JWT access token for immediate authentication.",
    tags=["Authentication"]
)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user and returns a JWT access token.

    Args:
        user_data (UserCreate): User registration data validated via a Pydantic schema.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: A dictionary containing the JWT access token and token type.
    """

    jwt_token = register_user(db, user_data)

    return {"access_token": jwt_token, "token_type": "bearer"}


@router.get(
    "/me",
    response_model=UserBase,
    summary="Get current user info",
    description="Returns information about the currently authenticated user based on the provided JWT token.",
    tags=["Authentication"]
)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Retrieves data of the currently authenticated user.

    Args:
        current_user (User): The currently authenticated user, provided via dependency injection.

    Returns:
        dict: A dictionary containing the user's basic information (username, email, role).
    """

    return {"username": current_user.username,
            "email": current_user.email,
            "role": current_user.role}
