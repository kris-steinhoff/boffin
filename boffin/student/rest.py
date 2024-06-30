from fastapi import APIRouter

from boffin.student import StudentId, service
from boffin.student.model import Student

router = APIRouter(prefix="/student", tags=["people"])


@router.post("/")
async def create_student(first_name: str, last_name: str) -> Student:
    student = await service.create_student(first_name=first_name, last_name=last_name)
    return student


@router.get("/")
async def list_students() -> list[Student]:
    return await service.list_students()


@router.get("/{student_id}")
async def get_student(student_id: StudentId) -> Student | None:
    return await service.get_student(student_id)


@router.put("/{student_id}")
async def update_student(
    student_id: StudentId,
    first_name: str | None = None,
    last_name: str | None = None,
) -> Student | None:
    return await service.update_student(
        student_id=student_id,
        first_name=first_name,
        last_name=last_name,
    )


@router.delete("/{student_id}")
async def delete_student(student_id: StudentId) -> None:
    return await service.delete_student(student_id)
