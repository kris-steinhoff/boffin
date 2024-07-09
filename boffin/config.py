from functools import cache, cached_property

import redis.asyncio as redis
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import Engine, create_engine


class Settings(BaseSettings):
    database_url: str
    redis_url: str

    server_host: str = "0.0.0.0"
    server_port: int = 8000
    server_workers: int = 1
    server_reload: bool = False

    dev_mode: bool = False

    @cached_property
    def redis_client(self) -> redis.Redis:
        return redis.from_url(self.redis_url)

    @cached_property
    def database_engine(self) -> Engine:
        return create_engine(self.database_url)

    model_config = SettingsConfigDict(env_file=".env")


@cache
def get_settings() -> Settings:
    return Settings()
