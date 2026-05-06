from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config import settings

if "sqlite" in settings.database_url:
    engine = create_engine(
        settings.database_url.replace("sqlite+aiosqlite://", "sqlite://"),
        connect_args={"check_same_thread": False},
    )
else:
    engine = create_engine(settings.database_url, pool_recycle=3600, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
