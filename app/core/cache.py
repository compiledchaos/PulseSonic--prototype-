# app/core/cache.py
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# Base class for ORM models
Base = declarative_base()


# Example Track model
class Downloaded(Base):
    __tablename__ = "downloaded"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    jamendo_id = Column(String, unique=True, index=True)
    title = Column(String)
    artist = Column(String)
    album = Column(String, nullable=True)
    cover_url = Column(String, nullable=True)
    stream_url = Column(String, nullable=True)


class User_Info(Base):
    """
    Stores basic user credentials.

    Note: For production, do NOT store plaintext passwords. Use a hashed password
    and proper authentication flow. This is kept simple to match current needs.
    """

    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    favorite = Column(String)  # JSON string of jamendo_id
    history = Column(String)  # JSON string of jamendo_id

    def __repr__(self) -> str:
        return f"<User_Info id={self.id} username={self.username!r}>"


# SQLite engine (file-based)
engine = create_engine("sqlite:///app_cache.db", echo=True)

# Session factory
SessionLocal = sessionmaker(bind=engine)


# Create tables if they don’t exist
def init_db():
    Base.metadata.create_all(bind=engine)
