

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db.models.base import Base


class Race(Base):
    __tablename__ = 'races'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(unique=True)
    year: Mapped[int] = mapped_column()

    def __repr__(self) -> str:
        return f"Race(id: {self.id}, {self.name}, {self.year})"
