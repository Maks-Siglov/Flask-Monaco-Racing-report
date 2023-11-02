from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, func, DateTime
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime

from app.db.models.base import Base


class Driver(Base):
    __tablename__ = 'drivers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    abr: Mapped[str] = mapped_column(String(5))
    name: Mapped[str] = mapped_column(String(30))
    team: Mapped[str] = mapped_column(String(50))

    result = relationship('Result', back_populates='driver')


class Result(Base):
    __tablename__ = 'results'

    id: Mapped[int] = mapped_column(primary_key=True)
    driver_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('drivers.id'))
    start: Mapped[datetime] = mapped_column(DateTime)
    end: Mapped[datetime] = mapped_column(DateTime)
    position: Mapped[int] = mapped_column(Integer, nullable=True)

    driver = relationship('Driver', back_populates='result')

    @hybrid_property
    def total_seconds(self) -> int:
        return (self.end - self.start).total_seconds()

    @total_seconds.expression
    def time_difference(cls) -> int:
        return (func.julianday(cls.end) - func.julianday(cls.start)) * 86400

    @property
    def result(self):
        minutes, seconds = divmod(self.total_seconds, 60)
        return int(minutes), round(seconds, 3)
