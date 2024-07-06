from functools import cache, cached_property

import redis.asyncio as redis
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    redis_url: str

    @cached_property
    def redis_client(self) -> redis.Redis:
        return redis.from_url(self.redis_url)


@cache
def get_settings() -> Settings:
    return Settings()
