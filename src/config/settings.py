from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # LLM
    llm_provider: str = "openai"            # openai | ollama
    llm_model: str = "gpt-4o-mini"
    llm_base_url: str = ""                  # для Ollama: http://ollama:11434/v1
    llm_temperature: float = 0.0

    # Embeddings
    embedding_provider: str = "openai"
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536
    embedding_base_url: str = ""

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