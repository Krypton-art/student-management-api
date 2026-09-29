from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.student import Student
from app.schemas.student import StudentCreate


def create_student(db: Session, student_data: StudentCreate):
    new_student = Student(
        name=student_data.name,
        age=student_data.age,
        branch=student_data.branch
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


def get_students(
    db: Session,
    branch: str | None = None
):
    statement = select(Student)

    if branch:
        statement = statement.where(
            Student.branch == branch
        )

    return db.scalars(statement).all()


def get_student(db: Session, student_id: int):
    return db.get(Student, student_id)


def update_student(
    db: Session,
    student_id: int,
    student_data: StudentCreate
):
    student = db.get(Student, student_id)

    if not student:
        return None

    student.name = student_data.name
    student.age = student_data.age
    student.branch = student_data.branch

    db.commit()
    db.refresh(student)

    return student


def delete_student(db: Session, student_id: int):
    student = db.get(Student, student_id)

    if not student:
        return False

    db.delete(student)
    db.commit()

    return True