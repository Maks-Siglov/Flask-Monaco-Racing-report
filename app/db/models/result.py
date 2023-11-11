

from datetime import datetime

from sqlalchemy import (
    Cast,
    ForeignKey,
    ColumnElement,
    Float,
)
from sqlalchemy.orm import (
    Mapped,
    relationship,
    mapped_column,
)
from sqlalchemy.ext.hybrid import hybrid_property


from app.db.models.base import Base
from app.db.models.driver import Driver
from app.db.models.race import Race
from app.db.models.stage import Stage


class Result(Base):
    __tablename__ = 'results'

    start: Mapped[datetime] = mapped_column()
    end: Mapped[datetime] = mapped_column()
    position: Mapped[int] = mapped_column(nullable=True)

    driver_id: Mapped[int] = mapped_column(
        ForeignKey('drivers.id', ondelete='CASCADE'), primary_key=True
    )
    driver: Mapped['Driver'] = relationship()

    race_id: Mapped[int] = mapped_column(ForeignKey(
        'races.id', ondelete='CASCADE'), primary_key=True
    )
    race: Mapped['Race'] = relationship()

    stage_id: Mapped[int] = mapped_column(ForeignKey(
        'stages.id', ondelete='CASCADE'), primary_key=True
    )
    stage: Mapped['Stage'] = relationship()

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
