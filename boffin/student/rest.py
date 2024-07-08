from fastapi import APIRouter

from boffin.student import StudentId, services
from boffin.student.models import Student

router = APIRouter(prefix="/student", tags=["people"])


@router.post("/")
async def create_student(first_name: str, last_name: str) -> Student:
    student = await services.create_student(first_name=first_name, last_name=last_name)
    return student


@router.get("/")
async def list_students() -> list[Student]:
    return await services.list_students()


@router.get("/{student_id}")
async def get_student(student_id: StudentId) -> Student | None:
    return await services.get_student(student_id)


@router.put("/{student_id}")
async def update_student(
    student_id: StudentId,
    first_name: str | None = None,
    last_name: str | None = None,
) -> Student | None:
    return await services.update_student(
        student_id=student_id,
        first_name=first_name,
        last_name=last_name,
    )


@router.delete("/{student_id}")
async def delete_student(student_id: StudentId) -> None:
    return await services.delete_student(student_id)
