import strawberry

from boffin.student import StudentId, service
from boffin.student.model import Student
from boffin.student.rest import list_students


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
    student = await service.get_student(StudentId(student_id))
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
        student = await service.create_student(first_name, last_name)
        return StudentType.from_pydantic(student)
