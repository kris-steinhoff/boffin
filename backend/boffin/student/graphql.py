from typing import AsyncGenerator, assert_never

import strawberry
from result import Err, Ok

from boffin.config import get_settings
from boffin.student import StudentId, services
from boffin.student.models import Student as StudentModel
from boffin.student.rest import list_students
from boffin.student.types import StudentDataEvent as StudentDataEventModel


@strawberry.experimental.pydantic.type(model=StudentModel)
class Student:
    id: strawberry.ID
    first_name: strawberry.auto
    last_name: strawberry.auto

    @classmethod
    def from_model(cls, student: StudentModel) -> "Student":
        return Student(
            id=str(student.id),
            first_name=student.first_name,
            last_name=student.last_name,
        )


async def resolve_student(student_id: str) -> Student:
    match result := await services.get_student(StudentId(student_id)):
        case Ok(student):
            return Student.from_model(student)
        case Err(error):
            raise error
        case _:
            assert_never(result)


async def resolve_studentes() -> list[Student]:
    studentes = await list_students()
    return [Student.from_pydantic(student) for student in studentes]


@strawberry.type
class StudentQuery:
    student: Student = strawberry.field(resolver=resolve_student)
    students: list[Student] = strawberry.field(resolver=resolve_studentes)


@strawberry.type
class StudentMutation:
    @strawberry.mutation
    async def create_student(self, first_name: str, last_name: str) -> Student:
        match result := await services.create_student(first_name, last_name):
            case Ok(student):
                return Student.from_model(student)
            case Err(ex):
                raise ex
            case _:
                assert_never(result)


@strawberry.experimental.pydantic.type(model=StudentDataEventModel, all_fields=True)
class StudentDataEvent:
    pass


@strawberry.type
class StudentSubscription:
    @strawberry.subscription
    async def student_modifications(self) -> AsyncGenerator[StudentDataEvent, None]:
        client = get_settings().redis_client
        async with client.pubsub(ignore_subscribe_messages=True) as pubsub:
            await pubsub.subscribe(StudentDataEventModel.get_channel_name())
            async for message in pubsub.listen():
                if message is None:
                    continue
                event = StudentDataEventModel.model_validate_json(message["data"])
                yield StudentDataEvent.from_pydantic(event)
