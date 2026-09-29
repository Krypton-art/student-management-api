from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Student as StudentModel

app = FastAPI()


class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(gt=0, lt=100)
    branch: str


class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    branch: str

    model_config = {"from_attributes": True}


@app.get("/")
def home():
    return {"message": "Student Management API"}


@app.post(
    "/students",
    status_code=status.HTTP_201_CREATED,
    response_model=StudentResponse
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    new_student = StudentModel(
        name=student.name,
        age=student.age,
        branch=student.branch
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


@app.get(
    "/students",
    response_model=list[StudentResponse]
)
def get_students(
    branch: str | None = None,
    db: Session = Depends(get_db)
):
    statement = select(StudentModel)

    if branch:
        statement = statement.where(
            StudentModel.branch == branch
        )

    return db.scalars(statement).all()


@app.get(
    "/students/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.get(StudentModel, student_id)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return student

@app.put(
    "/students/{student_id}",
    response_model=StudentResponse
)
def update_student(
    student_id: int,
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    existing_student = db.get(StudentModel, student_id)

    if not existing_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    existing_student.name = student.name
    existing_student.age = student.age
    existing_student.branch = student.branch

    db.commit()
    db.refresh(existing_student)

    return existing_student

@app.delete(
    "/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.get(StudentModel, student_id)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return