from dataclasses import dataclass
from .Stop import Stop


@dataclass
class PathStop:
    """represent the way between 2 bus stops"""

    start: Stop
    end: Stop
    distance: float
    time: float
    path: list[tuple[float, float]]
