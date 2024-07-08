from sqlmodel import SQLModel

from boffin.common.models import (
    CreatedAtMixin,
    PrefixedID,
    UpdatedAtMixin,
    primary_key_prefixed_short_uuid,
)


class Student(SQLModel, CreatedAtMixin, UpdatedAtMixin, table=True):
    id: PrefixedID = primary_key_prefixed_short_uuid("student")
    first_name: str
    last_name: str
