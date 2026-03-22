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
    embedding_provider: str = "huggingface"
    embedding_model: str = "intfloat/multilingual-e5-large-instruct"
    embedding_dimensions: int = 1024
    embedding_base_url: str = ""
    ollama_base_url: str = "http://host.docker.internal:11434"
    huggingface_cache_dir: str = "/app/.cache/huggingface"  # путь внутри контейнера

    # OpenAI
    openai_api_key: str = ""

    # GoogleAI
    google_api_key: str = ""

    # Database
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "postgres"
    db_password: str = "secret"
    db_name: str = "avtobot"

    # App
    app_env: str = "development"
    log_level: str = "INFO"

    @property
    def async_db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def sync_db_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

settings = Settings()