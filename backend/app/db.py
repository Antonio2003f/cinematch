import redis
from qdrant_client import QdrantClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    password=settings.redis_password,
    decode_responses=True,
)

qdrant_client = QdrantClient(
    host=settings.qdrant_host,
    port=settings.qdrant_port,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
