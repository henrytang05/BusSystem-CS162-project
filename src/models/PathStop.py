from dataclasses import dataclass
from .Stop import StopData


@dataclass
class PathStop:
    """represent the way between 2 bus stops"""

    start: StopData
    end: StopData
    distance: float
    time: float
    path: list[tuple[float, float]]
