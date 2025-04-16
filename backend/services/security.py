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
    Hash a given password and return it.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """

    return pwd_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password (str): The plain password to verify.
        hashed_password (str): The hashed password from the database.

    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.

    Raises:
        VerifyMismatchError: If the plain password does not match the hashed password.
        Exception: If there's an issue with the password verification (e.g., corrupted hash or other unexpected error).
    """

    try:
        pwd_hash.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        raise VerifyMismatchError("Password does not match the stored hash!")
    except Exception as e:
        raise Exception(f"Error during verification: {e}")


load_dotenv()
ALGORITHM = os.getenv('ALGORITHM')
SECRET_KEY = os.getenv('SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')


def create_access_token(data: dict, expires_delta=timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))) -> str:
    """
    Creates a JWT access token with an expiration time.

    Args:
        data (dict): The data to encode into the JWT's payload.
        expires_delta (timedelta): The time duration until the token expires. Default is set from ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
        str: The encoded JWT access token as a string.

    Raises:
        jwt.PyJWTError: If there is an issue with encoding the token (e.g., invalid secret key, algorithm error).
    """

    to_encode = data.copy()
    expire = datetime.now(UTC) + expires_delta
    to_encode.update({'exp': expire})
    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_token


def verify_access_token(token: str) -> dict:
    """
    Verifies given JWT access token.

    Args:
        token (str): The JWT access token.

    Returns:
        dict: The decoded JWT access token if successful, None otherwise.

    Raises:
        jwt.ExpiredSignatureError: If the token is expired.
        jwt.InvalidTokenError: If the token is invalid.
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
