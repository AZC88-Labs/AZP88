from sqlalchemy.orm import Session
from backend.models.users import User
from backend.schemas.users import UserLogin
from security import verify_password, create_access_token
from fastapi import HTTPException, status

def login_user(db: Session, credentials: UserLogin):
    """
    Validates user login credentials and returns a JWT access token.

    :param db: SQLAlchemy database session
    :param credentials: Pydantic schema containing user's email and password
    :return: JWT access token as a string
    :raises HTTPException: if credentials are invalid
    """
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, str(user.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    jwt_token = create_access_token(data={"sub": credentials.id})

    return {"access_token": jwt_token, "token_type": "bearer"}