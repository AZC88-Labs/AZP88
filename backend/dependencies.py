from argon2 import PasswordHasher
from argon2.exceptions import VerificationError

pwd_hash = PasswordHasher()


def hash_password(password: str) -> str:
    """
    Hashes the given password using a secure hashing algorithm and returns the hashed result.

    :param password: The plain-text password that needs to be hashed.
    :type password: str
    :return: The hashed password as a string.
    :rtype: str
    """
    return pwd_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies the given password against the given hashed password. Returns `True` if the hashed password matches, otherwise `False`.

    :param password: Password given by the user.
    :type password: str
    :param hashed_password: Stored hashed password in the database.
    :type hashed_password: str
    :return: Result of the password verification.
    :rtype: bool
    """
    try:
        pwd_hash.verify(password, hashed_password)
        return True
    except VerificationError:
        return False
