import json

import pika
from qdrant_client.models import PointStruct
from sentence_transformers import SentenceTransformer

from app.config import settings
from app.db import qdrant_client

_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.embedding_model)
    return _model


def process_message(ch, method, properties, body):
    data = json.loads(body)
    movie_id = data["movie_id"]
    title = data["title"]
    plot = data["plot"]

    print(f"Procesez film {movie_id}: {title}")

    model = get_model()
    vector = model.encode(plot).tolist()

    qdrant_client.upsert(
        collection_name=settings.qdrant_collection,
        points=[PointStruct(id=movie_id, vector=vector, payload=data)],
    )

    print(f"Embedding generat si salvat pentru filmul {movie_id}.")
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