from sqlalchemy import select

from database import SessionLocal
from models import Student


with SessionLocal() as db:
    statement = select(Student)

    students = db.scalars(statement).all()

    for student in students:
        print(
            student.id,
            student.name,
            student.age,
            student.branch
        )