from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.

    Inherit from this class to define database models. This is the declarative base used by SQLAlchemy.
    """

    pass


def get_db():
    """
    Yields a database session to be used in a dependency context.

    This function is intended to be used with FastAPI's dependency injection system.
    It ensures that the database session is properly closed after the request is handled.

    Yields:
        Session: SQLAlchemy database session.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
