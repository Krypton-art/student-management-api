from fastapi import FastAPI, HTTPException , status
from pydantic import BaseModel , Field

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

students = []
next_student_id = 1


@app.get("/")
def home():
    return {"message": "Student Management API"}


@app.post(
    "/students",
    status_code=status.HTTP_201_CREATED,
    response_model=StudentResponse
)
def create_student(student: StudentCreate):
    global next_student_id

    student_data = student.model_dump()
    student_data["id"] = next_student_id

    students.append(student_data)
    next_student_id += 1

    return student_data


@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Student not found"
)

@app.get("/students", response_model=list[StudentResponse])
def get_students(branch: str | None = None):
    if branch:
        return [student for student in students if student["branch"] == branch]

    return students

@app.put(
    "/students/{student_id}",
    response_model=StudentResponse
)
def update_student(student_id: int, student: StudentCreate):

    for existing_student in students:
        if existing_student["id"] == student_id:

            existing_student["name"] = student.name
            existing_student["age"] = student.age
            existing_student["branch"] = student.branch

            return existing_student

    raise HTTPException(
        status_code=404,
        detail="Student not found"
    )

@app.delete(
    "/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_student(student_id: int):
    for index, student in enumerate(students):
        if student["id"] == student_id:
            students.pop(index)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )