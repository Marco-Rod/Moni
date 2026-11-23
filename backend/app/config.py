from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    database_url: str = "postgresql+psycopg://finanzas:cambia_esto@db:5432/finanzas"
    ollama_base_url: str = "http://ollama:11434"
    llm_model: str = "qwen2.5:7b"
    embedding_model: str = "bge-m3"
    embedding_dim: int = 1024
    default_currency: str = "MXN"


settings = Settings()
