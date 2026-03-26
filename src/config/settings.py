# src/config/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # LLM
    LLM_PROVIDER: str = "ollama"
    LLM_MODEL: str = "mistral"
    OLLAMA_BASE_URL: str = "http://host.docker.internal:11434"
    OPENAI_API_KEY: str | None = None

    # Embeddings
    EMBEDDING_PROVIDER: str = "huggingface"
    EMBEDDING_MODEL: str = "intfloat/multilingual-e5-large-instruct"
    EMBEDDING_DIMENSIONS: int = 1024
    EMBEDDING_BASE_URL: str = ""
    HUGGINGFACE_CACHE_DIR: str = "/app/.cache/huggingface"

    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "secret"
    DB_NAME: str = "avtobot"

    # App
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"

    @property
    def async_db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

settings = Settings()