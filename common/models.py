import datetime
from uuid import UUID

from sqlmodel import Field, SQLModel


def _utc_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


class BaseModel(SQLModel):
    id: UUID = Field(primary_key=True)
    created_at: datetime.datetime = Field(default_factory=_utc_now)
    updated_at: datetime.datetime = Field(default_factory=_utc_now)
