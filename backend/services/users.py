from argon2 import PasswordHasher
from sqlalchemy.orm import Session
from ..models.users import User
from ..schemas.users import UserLogin, UserCreate
from .security import verify_password, create_access_token, hash_password
from fastapi import HTTPException, status
from ..models.enums import UserRole


def login_user(db: Session, credentials: UserLogin):
    """
    TODO
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


def register_user(db: Session, credential: UserCreate):
    """
    TODO
    """

    check_email = db.query(User).filter(User.email == credential.email).first()
    if check_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered"
        )

    check_username = db.query(User).filter(User.username == credential.username).first()
    if check_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already taken"
        )

    new_user = User(
        email=credential.email,
        username=credential.username,
        password=hash_password(credential.password),
        role=UserRole.user
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    jwt_token = create_access_token(data={"sub": new_user.id})

    return jwt_token
