

from sqlalchemy import (String)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db.models.base import Base


class Driver(Base):
    __tablename__ = 'drivers'

    id: Mapped[int] = mapped_column(primary_key=True)

    abbr: Mapped[str] = mapped_column(String(5))
    name: Mapped[str] = mapped_column(String(30))
    team: Mapped[str] = mapped_column(String(50))
