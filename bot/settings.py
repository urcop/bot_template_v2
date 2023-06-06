from pydantic import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    DB_DSN: str
    REDIS_DSN: str | None = None
