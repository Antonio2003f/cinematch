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

    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    class Config:
        env_file = ".env"


settings = Settings()
