

from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db.models.base import Base


class Stage(Base):
    __tablename__ = 'stages'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(10), unique=True)

    def __repr__(self) -> str:
        return f"Stage(id: {self.id}, {self.name})"
