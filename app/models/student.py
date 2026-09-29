from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    age: Mapped[int] = mapped_column(
        nullable=False
    )

    branch: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )