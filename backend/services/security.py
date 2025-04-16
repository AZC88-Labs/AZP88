from datetime import timedelta, datetime, UTC
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from dotenv import load_dotenv
import os
import jwt
from fastapi import HTTPException

pwd_hash = PasswordHasher()


def hash_password(password: str) -> str:
    """
    TODO
    """
    return pwd_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    TODO
    """

    try:
        pwd_hash.verify(hashed_password, plain_password)
        return True
    except Exception as e:
        print(e)
        return False


load_dotenv()
ALGORITHM = os.getenv('ALGORITHM')
SECRET_KEY = os.getenv('SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')


def create_access_token(data: dict, expires_delta=timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))) -> str:
    """
    TODO
    """

    to_encode = data.copy()
    expire = datetime.now(UTC) + expires_delta
    to_encode.update({'exp': expire})
    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_token


def verify_access_token(token: str) -> dict:
    """
    TODO
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
