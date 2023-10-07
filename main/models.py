from main.utils.utils import LapTime
from dataclasses import dataclass


@dataclass
class Driver:
    abr: str
    name: str
    team: str
    lap_time: LapTime
    position: int | None = None
