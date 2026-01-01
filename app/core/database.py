from typing import Generator
from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

# Create sync engine for Vercel serverless
engine = create_engine(
    settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql+psycopg2://"),
    echo=settings.ENVIRONMENT == "development",
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=0,
)

def get_engine():
    """Get sync database engine"""
    return engine

def get_session() -> Generator[Session, None, None]:
    """Dependency for getting database session"""
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

def create_db_and_tables():
    """Create database tables (for testing/init)"""
    SQLModel.metadata.create_all(engine)
