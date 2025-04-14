from requests import Session
from ..dependencies import get_current_user
from ..models.users import User
from ..services.users import login_user, register_user
from fastapi import Depends, APIRouter
from ..db import get_db
from ..schemas.users import UserLogin, UserCreate, UserBase

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login a user and return a JWT access token.

    :param user_data: Pydantic schema containing user's email and password.
    password must contain at least one uppercase letter, one digit, and one special character.
    :param db: SQLAlchemy database session
    :return: JWT access token.
    """

    jwt_token = login_user(db, user_data)

    return {"access_token": jwt_token, "token_type": "bearer"}


@router.put("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    TODO
    :param user_data:
    :param db:
    :return:
    """

    jwt_token = register_user(db, user_data)

    return {"access_token": jwt_token, "token_type": "bearer"}


@router.get("/me", response_model=UserBase)
def get_me(current_user: User = Depends(get_current_user)):
    """
    TODO
    :param current_user:
    :return:
    """
    return {"username": current_user.username, "email": current_user.email, "role": current_user.role}
