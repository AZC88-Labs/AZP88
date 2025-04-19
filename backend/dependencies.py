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
    Retrieves the current authenticated user from the database using the provided JWT access token.

    Args:
        token (str): JWT access token, extracted from the Authorization header.
        db (Session): SQLAlchemy session for database interaction.

    Returns:
        User: The currently authenticated user object.

    Raises:
        HTTPException:
            - 400 if the token is missing the 'sub' claim.
            - 404 if the user with the given ID is not found in the database.
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
