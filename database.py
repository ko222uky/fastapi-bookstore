"""
Example database connection using SQLAlchemy.
"""
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from sqlalchemy import create_engine




DATABASE_URL = r"sqlite:///./test.db"
engine = create_engine(DATABASE_URL)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    name: Mapped[str]
    email: Mapped[str]

# proceeds to create tables in the database.
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
