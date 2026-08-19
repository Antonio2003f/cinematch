import json
from pathlib import Path

from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

from app.config import settings
from app.db import engine, SessionLocal, qdrant_client
from app.models import Base, Movie

DATA_PATH = Path(__file__).parent / "movies.json"


def load_movies() -> list[dict]:
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


def seed_postgres(movies: list[dict]) -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing_ids = {row[0] for row in db.query(Movie.id).all()}
        new_movies = [m for m in movies if m["id"] not in existing_ids]

        db.bulk_insert_mappings(Movie, [
            {
                "id": m["id"], "title": m["title"], "year": m["year"],
                "director": m["director"], "genre": m["genre"],
                "rating": m["rating"], "plot": m["plot"],
                "poster_url": f"https://placehold.co/300x450/1a1a2e/eee?text={m['title'].replace(' ', '+')[:40]}",
            }
            for m in new_movies
        ])
        db.commit()
        print(f"Postgres: {len(new_movies)} filme noi inserate ({len(movies) - len(new_movies)} existau deja).")
    finally:
        db.close()


def seed_qdrant(movies: list[dict]) -> None:
    print(f"Incarc modelul de embeddings: {settings.embedding_model}")
    model = SentenceTransformer(settings.embedding_model)
    vector_size = model.get_sentence_embedding_dimension()

    qdrant_client.recreate_collection(
        collection_name=settings.qdrant_collection,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
    )

    plots = [m["plot"] for m in movies]
    print("Generez embeddings pentru plot-uri...")
    vectors = model.encode(plots, show_progress_bar=True)

    points = [
        PointStruct(
            id=m["id"],
            vector=vec.tolist(),
            payload={
                "id": m["id"], "title": m["title"], "year": m["year"],
                "director": m["director"], "genre": m["genre"],
                "rating": m["rating"], "plot": m["plot"],
                "poster_url": f"https://placehold.co/300x450/1a1a2e/eee?text={m['title'].replace(' ', '+')[:40]}",
            },
        )
        for m, vec in zip(movies, vectors)
    ]

    batch_size = 256
    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        qdrant_client.upsert(collection_name=settings.qdrant_collection, points=batch)
        print(f"  upsert {i + len(batch)}/{len(points)}")

    print(f"Qdrant: {len(points)} vectori incarcati in colectia '{settings.qdrant_collection}'.")


if __name__ == "__main__":
    movies = load_movies()
    seed_postgres(movies)
    seed_qdrant(movies)
    print("Seed complet.")
