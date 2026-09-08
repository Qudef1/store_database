from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Банк данных технологий создания продуктов"
    debug: str = "false"

    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "food_products"
    db_user: str = "postgres"
    db_password: str = "postgres"

    @property
    def is_debug(self) -> bool:
        return self.debug.lower() in ("1", "true", "yes", "on")

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()