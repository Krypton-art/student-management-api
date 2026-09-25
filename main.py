from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Student(BaseModel):
    name: str
    age: int
    branch: str


students = []


@app.get("/")
def home():
    return {"message": "Student Management API"}


@app.post("/students")
def create_student(student: Student):
    student_data = student.model_dump()
    student_data["id"] = len(students) + 1

    students.append(student_data)

    return student_data


@app.get("/students")
def get_students():
    return students

@app.get("/students/{student_id}")
def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(status_code=404, detail="Student not found")