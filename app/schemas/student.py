from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(gt=0, lt=100)
    branch: str = Field(min_length=2, max_length=30)


class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    branch: str

    model_config = {"from_attributes": True}