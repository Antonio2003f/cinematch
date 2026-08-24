from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_db: str
    postgres_user: str
    postgres_password: str

    redis_host: str = "redis"
    redis_port: int = 6379
    redis_password: str

    qdrant_host: str = "qdrant"
    qdrant_port: int = 6333
    qdrant_collection: str = "movies"

    rabbitmq_host: str = "rabbitmq"
    rabbitmq_port: int = 5672
    rabbitmq_user: str = "cinematch"
    rabbitmq_password: str
    rabbitmq_queue: str = "movie_ingestion"

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def rabbitmq_url(self) -> str:
        return f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}@{self.rabbitmq_host}:{self.rabbitmq_port}/"

    class Config:
        env_file = ".env"


settings = Settings()