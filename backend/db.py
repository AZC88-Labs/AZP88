from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, DeclarativeBase

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost/AZP88_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = DeclarativeBase()


def get_db():
    """
    Provides a database session for use in requests or operations.

    :return: a database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
