from fastapi import FastAPI

from app.routes.students import router as student_router


app = FastAPI(
    title="Student Management API",
    version="1.0.0"
)


@app.get(
    "/",
    response_model=dict[str, str]
)
def home():
    return {"message": "Student Management API"}


app.include_router(student_router)