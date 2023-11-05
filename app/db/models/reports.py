

from datetime import datetime

from sqlalchemy import (
    String,
    ForeignKey,
    ColumnElement,
    Cast,
    Float
)
from sqlalchemy.orm import (
    Mapped,
    relationship,
    mapped_column,
)
from sqlalchemy.ext.hybrid import hybrid_property


from app.db.models.base import Base


class Driver(Base):
    __tablename__ = 'drivers'

    id: Mapped[int] = mapped_column(primary_key=True)
    abbr: Mapped[str] = mapped_column(String(5))
    name: Mapped[str] = mapped_column(String(30))
    team: Mapped[str] = mapped_column(String(50))

    result: Mapped['Result'] = relationship(back_populates='driver')


class Result(Base):
    __tablename__ = 'results'

    id: Mapped[int] = mapped_column(primary_key=True)
    driver_id: Mapped[int] = mapped_column(
        ForeignKey('drivers.id', ondelete='RESTRICT')
    )
    start: Mapped[datetime] = mapped_column()
    end: Mapped[datetime] = mapped_column()
    position: Mapped[int] = mapped_column(nullable=True)

    driver: Mapped['Driver'] = relationship(back_populates='result')

    @hybrid_property
    def total_seconds(self) -> float:
        return (self.end - self.start).total_seconds()

    @total_seconds.inplace.expression
    def time_difference(cls) -> ColumnElement[float]:
        return Cast((cls.end - cls.start), type_=Float)

    @property
    def result(self) -> tuple[int, float]:
        minutes, seconds = divmod(self.total_seconds, 60)
        return int(minutes), round(seconds, 3)
