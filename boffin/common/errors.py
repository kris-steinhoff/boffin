from dataclasses import dataclass


class DataError(Exception):
    pass


@dataclass
class DoesNotExist(DataError):
    object_id: str

    def __str__(self):
        return f"{self.object_id} does not exist"


class AlreadyExists(DataError):
    pass
