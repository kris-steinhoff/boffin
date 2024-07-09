from typing import AsyncGenerator

import strawberry

from boffin.config import get_settings
from boffin.student import StudentId, services
from boffin.student.models import Student
from boffin.student.rest import list_students
from boffin.student.types import StudentDataEvent


@strawberry.experimental.pydantic.type(model=Student)
class StudentType:
    id: strawberry.ID
    first_name: strawberry.auto
    last_name: strawberry.auto

    @classmethod
    def from_model(cls, student: Student) -> "StudentType":
        return StudentType(
            id=str(student.id),
            first_name=student.first_name,
            last_name=student.last_name,
        )


async def resolve_student(student_id: str) -> StudentType | None:
    student = await services.get_student(StudentId(student_id))
    if student is None:
        return None
    return StudentType.from_pydantic(student)


async def resolve_studentes() -> list[StudentType]:
    studentes = await list_students()
    return [StudentType.from_pydantic(student) for student in studentes]


@strawberry.type
class StudentQuery:
    student: StudentType | None = strawberry.field(resolver=resolve_student)
    students: list[StudentType] = strawberry.field(resolver=resolve_studentes)


@strawberry.type
class StudentMutation:
    @strawberry.mutation
    async def create_student(self, first_name: str, last_name: str) -> StudentType:
        student = await services.create_student(first_name, last_name)
        return StudentType.from_pydantic(student)


@strawberry.experimental.pydantic.type(model=StudentDataEvent, all_fields=True)
class StudentDataEventType:
    pass


@strawberry.type
class StudentSubscription:
    @strawberry.subscription
    async def student_modifications(self) -> AsyncGenerator[StudentDataEventType, None]:
        client = get_settings().redis_client
        async with client.pubsub(ignore_subscribe_messages=True) as pubsub:
            await pubsub.subscribe(StudentDataEvent.get_channel_name())
            async for message in pubsub.listen():
                if message is None:
                    continue
                event = StudentDataEvent.model_validate_json(message["data"])
                yield StudentDataEventType.from_pydantic(event)
