import structlog
from sqlmodel import Session, select

from boffin.common.db import ENGINE
from boffin.student import StudentId
from boffin.student.model import Student
from boffin.student.types import StudentDataEvent

__all__ = [
    "create_student",
    "get_student",
    "list_students",
    "update_student",
    "delete_student",
]


logger = structlog.get_logger()


async def create_student(first_name: str, last_name: str) -> Student:
    student = Student(first_name=first_name, last_name=last_name)
    session = Session(ENGINE)
    session.add(student)
    session.commit()
    session.refresh(student)
    session.close()
    await StudentDataEvent.emit_created(str(student.id))
    logger.info("Student created", student_id=student.id)
    return student


async def get_student(student_id: StudentId) -> Student | None:
    session = Session(ENGINE)
    student = session.exec(
        select(Student).where(Student.id == student_id)
    ).one_or_none()
    session.close()

    return student


async def list_students() -> list[Student]:
    session = Session(ENGINE)
    result = session.exec(select(Student))
    studentes = [h for h in result]
    session.close()
    return studentes


async def update_student(
    student_id: str,
    first_name: str | None = None,
    last_name: str | None = None,
) -> Student | None:
    session = Session(ENGINE)
    student = session.get(Student, student_id)
    if student is None:
        return None

    if first_name is not None:
        student.first_name = first_name
    if last_name is not None:
        student.last_name = last_name

    session.add(student)
    session.commit()
    session.refresh(student)
    session.close()
    await StudentDataEvent.emit_updated(str(student.id))
    return student


async def delete_student(student_id: str) -> None:
    session = Session(ENGINE)
    student = session.get(Student, student_id)

    if student is None:
        return None

    session.delete(student)
    session.commit()
    session.close()
    await StudentDataEvent.emit_deleted(str(student.id))
    return None
