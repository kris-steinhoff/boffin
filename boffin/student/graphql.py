import strawberry

from boffin.student import StudentId
from boffin.student.model import Student
from boffin.student.rest import list_students
from boffin.student.service import get_student


@strawberry.experimental.pydantic.type(model=Student)
class StudentType:
    id: strawberry.ID
    first_name: strawberry.auto
    last_name: strawberry.auto


async def resolve_student(student_id: str) -> StudentType | None:
    student = await get_student(StudentId(student_id))
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
