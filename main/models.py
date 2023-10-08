from dataclasses import dataclass, field
from typing import Self


@dataclass
class LapTime:
    minutes: int
    seconds: float
    __for_sort: tuple[bool, tuple[int, float]] = field(init=False, repr=False)

    def __post_init__(self):
        self.__for_sort = (self.minutes <= 0, (abs(self.minutes), self.seconds))

    def __gt__(self, other: Self) -> bool:
        return self.__for_sort < other.__for_sort


@dataclass
class Driver:
    abr: str
    name: str
    team: str
    lap_time: LapTime
    position: int | None = None

    def __gt__(self, other: Self) -> bool:
        if self.position is not None:
            assert other.position
            return self.position < other.position

        return self.lap_time < other.lap_time
