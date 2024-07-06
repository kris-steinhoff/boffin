import strawberry

from boffin.common.types import DataEvent


@strawberry.experimental.pydantic.type(model=DataEvent, all_fields=True)
class DataEventType:
    pass
