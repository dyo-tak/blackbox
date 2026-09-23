"""blackbox configuration.

DB connection is env-driven and DB-independent. Everything defaults to
SQLite for zero-setup dev; set BLACKBOX_DB_URL for Postgres/MySQL.

Examples:
  sqlite:///blackbox.db
  postgresql+psycopg://user:pass@localhost:5432/blackbox
  mysql+pymysql://user:pass@localhost:3306/blackbox
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="BLACKBOX_", env_file=".env", extra="ignore"
    )

    db_url: str = "sqlite:///blackbox.db"
    db_echo: bool = False
    api_host: str = "127.0.0.1"
    api_port: int = 8000


settings = Settings()

# Canonical export: `from blackbox import config; config.db_url`
# (attribute access on the instance itself, no `.settings` hop)
config = settings

