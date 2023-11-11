

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db.models.base import Base


class Race(Base):
    __tablename__ = 'races'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(default='Monaco')
    year: Mapped[int] = mapped_column(default=2018)
