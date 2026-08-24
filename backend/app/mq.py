import json
import pika

from app.config import settings


def publish_movie_ingestion(movie_id: int, title: str, plot: str) -> None:
    params = pika.URLParameters(settings.rabbitmq_url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=settings.rabbitmq_queue, durable=True)

    message = json.dumps({"movie_id": movie_id, "title": title, "plot": plot})
    channel.basic_publish(
        exchange="",
        routing_key=settings.rabbitmq_queue,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2),  # persistent
    )
    connection.close()