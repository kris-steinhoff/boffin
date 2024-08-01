import uuid
from typing import Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from sqlalchemy import UUID, Column, DateTime, Dialect, TypeDecorator, func
from sqlalchemy.orm import declared_attr
from sqlmodel import Field

from boffin.common.base62 import Base62


class InvalidPrefixedID(ValueError):
    pass


class PrefixedID(TypeDecorator):
    impl = UUID(as_uuid=True)
    cache_ok = True

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(str))

    def __init__(self, prefix: str, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        if "_" in prefix:
            raise InvalidPrefixedID("Prefix cannot contain underscores")

        self.prefix = prefix

    def process_bind_param(self, value: Any | None, dialect: Dialect) -> Any:
        try:
            uuid_encoded = str(value).split("_")[1]
        except (IndexError, AttributeError):
            raise InvalidPrefixedID(
                "Invalid value for PrefixedID, must include an underscore "
                f"character: {value}"
            )
        try:
            return uuid.UUID(int=Base62.decode(uuid_encoded))
        except ValueError as exc:
            raise InvalidPrefixedID(f"Invalid value for PrefixedID, {exc}: {value}")

    def process_result_value(self, value: Any | None, dialect: Dialect) -> Any:
        try:
            if value is None:
                raise ValueError("Value is None")

            value_int = int(value)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid value for PrefixedShortUUID: {value}")

        return f"{self.prefix}_{Base62.encode(value_int)}"


def primary_key_prefixed_short_uuid(prefix: str) -> Any:
    def new_prefixed_short_uuid():
        return f"{prefix}_{Base62.encode(uuid.uuid4().int)}"

    return Field(
        default_factory=new_prefixed_short_uuid,
        sa_column=Column(PrefixedID(prefix), primary_key=True),
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
