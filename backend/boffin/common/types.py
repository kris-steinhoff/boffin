import datetime
from enum import Enum

import strawberry
from pydantic import BaseModel

from boffin.config import get_settings


@strawberry.enum
class EventType(str, Enum):
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"


class DataEvent(BaseModel):
    id: str
    event_type: EventType
    timestamp: datetime.datetime

    @classmethod
    def get_channel_name(self) -> str:
        return f"data_event:{self.__class__.__name__}"

    @classmethod
    async def emit(cls, id: str, event_type: EventType) -> None:
        event = cls(
            id=id,
            event_type=event_type,
            timestamp=datetime.datetime.now(tz=datetime.UTC),
        )
        redis_client = get_settings().redis_client
        await redis_client.publish(cls.get_channel_name(), event.model_dump_json())

    @classmethod
    async def emit_created(cls, id: str) -> None:
        return await cls.emit(id, EventType.CREATED)

    @classmethod
    async def emit_updated(cls, id: str) -> None:
        return await cls.emit(id, EventType.UPDATED)

    @classmethod
    async def emit_deleted(cls, id: str) -> None:
        return await cls.emit(id, EventType.DELETED)
