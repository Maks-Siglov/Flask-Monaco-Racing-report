

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.db.models.base import Base
from app.db.models.team import Team


class Driver(Base):
    __tablename__ = 'drivers'

    id: Mapped[int] = mapped_column(primary_key=True)

    abbr: Mapped[str] = mapped_column(String(5))
    name: Mapped[str] = mapped_column(String(30))

    team_id: Mapped[int] = mapped_column(ForeignKey(
        'teams.id', ondelete='CASCADE')
    )
    team: Mapped['Team'] = relationship()
