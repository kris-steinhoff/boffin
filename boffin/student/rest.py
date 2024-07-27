from typing import assert_never

from fastapi import APIRouter, HTTPException, status
from result import Err, Ok

from boffin.common.rest import get_responses_detail_dict
from boffin.student import StudentId, services
from boffin.student.models import Student

router = APIRouter(prefix="/student", tags=["people"])


@router.post("/")
async def create_student(first_name: str, last_name: str) -> Student:
    match result := await services.create_student(first_name, last_name):
        case Ok(student):
            return student
        case Err(ex):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(ex))
        case _:
            assert_never(result)


@router.get("/")
async def list_students() -> list[Student]:
    return await services.list_students()


@router.get(
    "/{student_id}", response_model=Student, responses=get_responses_detail_dict([404])
)
async def get_student(student_id: StudentId) -> Student:
    result = await services.get_student(student_id)
    match result:
        case Ok(student):
            return student
        case Err(ex):
            raise ex
        case _:
            assert_never(result)


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
