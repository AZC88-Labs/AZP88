from requests import Session
from ..services.users import login_user
from fastapi import Depends, APIRouter
from ..db import get_db
from ..schemas.users import UserLogin

router = APIRouter(tags=["Authentication"])


@router.post("/login")
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login a user and return a JWT access token.

    :param user_data: Pydantic schema containing user's email and password.
    password must contain at least one uppercase letter, one digit, and one special character.
    :param db: SQLAlchemy database session
    :return: JWT access token.
    """
    jwt_token = login_user(db, user_data)
    return {"access_token": jwt_token, "token_type": "bearer"}
