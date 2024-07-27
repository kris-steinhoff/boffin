from dataclasses import dataclass


class DataError(Exception):
    pass


@dataclass
class DoesNotExist(DataError):
    object_id: str


class AlreadyExists(DataError):
    pass
