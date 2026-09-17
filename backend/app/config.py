from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "fmucxkf"
    database_url: str = "postgresql+psycopg://fmucxkf:localdev@postgres:5432/fmucxkf"
    redis_url: str = "redis://redis:6379/0"
    publish_root: str = "/srv/published"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
