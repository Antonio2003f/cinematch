import json

import pika
from qdrant_client.models import PointStruct
from sentence_transformers import SentenceTransformer

from app.config import settings
from app.db import qdrant_client, SessionLocal
from app.models import Movie

_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.embedding_model)
    return _model


def process_message(ch, method, properties, body):
    data = json.loads(body)
    movie_id = data["movie_id"]

    db = SessionLocal()
    try:
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
    finally:
        db.close()

    if movie is None:
        print(f"Film {movie_id} nu a fost gasit in Postgres, sar peste.")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    print(f"Procesez film {movie.id}: {movie.title}")

    model = get_model()
    vector = model.encode(movie.plot or "").tolist()

    payload = {
        "id": movie.id,
        "title": movie.title,
        "year": movie.year,
        "director": movie.director,
        "genre": movie.genre,
        "rating": movie.rating,
        "plot": movie.plot,
        "poster_url": movie.poster_url,
    }

    qdrant_client.upsert(
        collection_name=settings.qdrant_collection,
        points=[PointStruct(id=movie.id, vector=vector, payload=payload)],
    )

    print(f"Embedding generat si salvat pentru filmul {movie.id}.")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    params = pika.URLParameters(settings.rabbitmq_url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=settings.rabbitmq_queue, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=settings.rabbitmq_queue, on_message_callback=process_message)

    print("Worker pornit, astept mesaje...")
    channel.start_consuming()


if __name__ == "__main__":
    main()