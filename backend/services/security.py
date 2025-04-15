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
    Hash a password and return it as a string

    :param password: plaint text password
    :return: hashed password
    """
    return pwd_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaint text password against the hashed password. Returns true if it matches, otherwise false.

    :param plain_password: plain text password given by user.
    :param hashed_password: hashed password from db.
    :return: True or False
    """
    try:
        pwd_hash.verify(plain_password, hashed_password)
        return True
    except VerifyMismatchError:
        return False


load_dotenv()
ALGORITHM = os.getenv('ALGORITHM')
SECRET_KEY = os.getenv('SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')


def create_access_token(data: dict, expires_delta=timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))) -> str:
    """
    Generate a JWT access token.

    :param data: The payload to encode into the token (usually user info like email or ID)
    :param expires_delta: Expiration time of the token (default: 1 hour)
    :return: JWT token as a string
    """

    to_encode = data.copy()
    expire = datetime.now(UTC) + expires_delta
    to_encode.update({'exp': expire})
    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_token


def verify_access_token(token: str) -> dict:
    """
    Verify the JWT token and return the payload if valid.

    :param token: JWT token as a string
    :return: Decoded payload if the token is valid
    :raises: jwt.ExpiredSignatureError if the token is expired
    :raises: jwt.InvalidTokenError if the token is invalid
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
