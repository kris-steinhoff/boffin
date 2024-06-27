import uuid
from typing import Any

from sqlalchemy import UUID, Column, DateTime, Dialect, TypeDecorator, func
from sqlalchemy.orm import declared_attr
from sqlmodel import Field

from common.base62 import Base62


class PrefixedShortUUID(TypeDecorator):
    impl = UUID

    def __init__(self, prefix: str, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        if "_" in prefix:
            raise ValueError("Prefix cannot contain underscores")

        self.prefix = prefix

    def process_bind_param(self, value: Any | None, dialect: Dialect) -> Any:
        uuid_encoded = str(value).split("_")[1]
        return Base62().decode(uuid_encoded)

    def process_result_value(self, value: Any | None, dialect: Dialect) -> Any:
        try:
            if value is None:
                raise ValueError("Value is None")

            value_int = int(value)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid value for PrefixedShortUUID: {value}")

        return f"{self.prefix}_{Base62().encode(value_int)}"


def primary_key_prefixed_short_uuid(prefix: str) -> Any:
    def new_prefixed_short_uuid():
        return Base62().encode(uuid.uuid4().int)

    return Field(
        default_factory=new_prefixed_short_uuid,
        sa_column=Column(PrefixedShortUUID(prefix), primary_key=True),
    )


class CreatedAtMixin:
    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), default=func.now(), nullable=False)


class UpdatedAtMixin:
    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime(timezone=True),
            default=func.now(),
            onupdate=func.now(),
            nullable=False,
        )
