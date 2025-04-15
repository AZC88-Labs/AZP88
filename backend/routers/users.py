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
    TODO
    """

    jwt_token = login_user(db, user_data)

    return {"access_token": jwt_token, "token_type": "bearer"}


@router.put("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    TODO
    """

    jwt_token = register_user(db, user_data)

    return {"access_token": jwt_token, "token_type": "bearer"}


@router.get("/me", response_model=UserBase)
def get_me(current_user: User = Depends(get_current_user)):
    """
    TODO
    """
    return {"username": current_user.username, "email": current_user.email, "role": current_user.role}
