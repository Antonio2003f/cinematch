import hashlib
import json

from sentence_transformers import SentenceTransformer

from app.config import settings
from app.db import qdrant_client, redis_client

_model: SentenceTransformer | None = None

CACHE_TTL_SECONDS = 3600


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.embedding_model)
    return _model


def _cache_key(query: str, limit: int) -> str:
    raw = f"{query.strip().lower()}:{limit}"
    return "search:" + hashlib.sha256(raw.encode()).hexdigest()


def semantic_search(query: str, limit: int = 12) -> tuple[list[dict], bool]:
    key = _cache_key(query, limit)

    cached = redis_client.get(key)
    if cached:
        return json.loads(cached), True

    model = get_model()
    vector = model.encode(query).tolist()

    hits = qdrant_client.search(
        collection_name=settings.qdrant_collection,
        query_vector=vector,
        limit=limit,
    )

    results = [
        {
            "id": hit.payload["id"],
            "title": hit.payload["title"],
            "year": hit.payload.get("year"),
            "director": hit.payload.get("director"),
            "genre": hit.payload.get("genre"),
            "rating": hit.payload.get("rating"),
            "plot": hit.payload.get("plot"),
            "poster_url": hit.payload.get("poster_url"),
            "score": hit.score,
        }
        for hit in hits
    ]

    redis_client.setex(key, CACHE_TTL_SECONDS, json.dumps(results))
    return results, False
