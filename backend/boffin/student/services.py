import structlog
from result import Err, Ok, Result
from sqlmodel import select

from boffin.common.db import get_session
from boffin.common.errors import DataError, DoesNotExist
from boffin.student import StudentId
from boffin.student.models import Student
from boffin.student.types import StudentDataEvent

__all__ = [
    "create_student",
    "get_student",
    "list_students",
    "update_student",
    "delete_student",
]


logger = structlog.get_logger()


async def create_student(first_name: str, last_name: str) -> Result[Student, DataError]:
    student = Student(first_name=first_name, last_name=last_name)
    with get_session() as session:
        session.add(student)
        session.commit()
        session.refresh(student)

    await StudentDataEvent.emit_created(str(student.id))
    logger.info("Student created", student_id=student.id)

    return Ok(student)


async def get_student(student_id: StudentId) -> Result[Student, DoesNotExist]:
    with get_session() as session:
        student = session.get(Student, student_id)
        if student is None:
            return Err(DoesNotExist(object_id=student_id))
        return Ok(student)


async def list_students() -> list[Student]:
    with get_session() as session:
        result = session.exec(select(Student))
        studentes = [h for h in result]

    return studentes


async def update_student(
    student_id: str,
    first_name: str | None = None,
    last_name: str | None = None,
) -> Result[Student, DataError]:
    with get_session() as session:
        student = session.get(Student, student_id)
        if student is None:
            return Err(DoesNotExist(object_id=student_id))

        if first_name is not None:
            student.first_name = first_name
        if last_name is not None:
            student.last_name = last_name

        session.add(student)
        session.commit()
        session.refresh(student)

    await StudentDataEvent.emit_updated(str(student.id))
    return Ok(student)


async def delete_student(student_id: str) -> Result[None, DataError]:
    with get_session() as session:
        student = session.get(Student, student_id)
        if student is None:
            return Err(DoesNotExist(object_id=student_id))
        session.delete(student)
        session.commit()

    await StudentDataEvent.emit_deleted(str(student.id))
    return Ok(None)
