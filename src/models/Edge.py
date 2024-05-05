__all__ = ["Edge"]

from geojson import LineString, Feature
from .RouteVar import Var
from .Stop import Stop


class Edge:
    def __init__(
        self,
        src: Stop,
        dest: Stop,
        time: float,
        path: list[tuple[float, float]],
        var: Var,
    ):
        self.src = src
        self.dest = dest
        self.time = time
        self.var = var
        self.path = path

    @property
    def src(self) -> int:
        return self._src.data.StopId

    @src.setter
    def src(self, value: Stop):
        self._src = value

    @property
    def dest(self) -> int:
        return self._dest.data.StopId

    @dest.setter
    def dest(self, value: Stop):
        self._dest = value

    def convert_to_geojson(self) -> list[Feature]:
        line = Feature(
            geometry=LineString(self.path),
            properties={
                "start": self.src,
                "end": self.dest,
                "stroke": "#ff0000",
            },
        )
        start = self._src.convert_to_geojson()
        end = self._dest.convert_to_geojson()

        return [line, start, end]

    def convert_var_to_geojson(self) -> list[Feature]:
        return self.var.convert_to_geojson()
