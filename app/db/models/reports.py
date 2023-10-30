from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Float

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

    driver_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('drivers.id'), primary_key=True)
    minutes: Mapped[int] = mapped_column(Integer)
    seconds: Mapped[float] = mapped_column(Float)
    position: Mapped[int] = mapped_column(Integer, nullable=True)

    driver = relationship('Driver', back_populates='result')

    @property
    def total_seconds(self):
        return round(self.minutes * 60 + self.seconds, 3)
