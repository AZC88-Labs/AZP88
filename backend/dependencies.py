from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from .db import get_db
from .models.users import User
from .services.security import verify_access_token

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')


def get_current_user(token: str = Depends(OAuth2PasswordBearer), db: Session = Depends(get_db)):
    """
    TODO
    :return:
    """

    try:
        payload = verify_access_token(token)
        userid: Optional[str] = payload.get('sub')

        if not userid:
            raise HTTPException(status_code=400, detail="Token is missing 'sub' claim")

    except HTTPException as e:
        raise e

    user = db.query(User).filter(User.id == userid).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user
