__all__ = ["Path"]

from dataclasses import dataclass
from ..utils import json_handler
from ..utils.constants import PATH_FILE


@dataclass
class PathData:
    lngs: list[float]
    lats: list[float]
    route: int
    var: int


class Path:

    # from .RouteVar import RouteVarHandler

    """A data class to represent a Path object"""

    def __init__(self, data: PathData):
        self.data = data

    @property
    def lng_lat_list(self) -> list[tuple[float, float]]:
        return list(zip(self.data.lngs, self.data.lats))


class PathLoader:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PathLoader, cls).__new__(cls)
        return cls._instance

    @property
    def data(self) -> dict[tuple[int, int], Path]:
        self._data = getattr(self, "_data", {})
        return self._data

    def load(self) -> dict[tuple[int, int], Path]:
        if self.data:
            return self.data
        from .RouteVar import RouteVarHandler

        _route_var_handler = RouteVarHandler()

        def add_path_to_route(routeid: int, varid: int, path: Path):
            _route_var_handler.get_var(routeid, varid).add_path(path.data)

        if not self.data:
            path_list: dict[tuple[int, int], Path] = {}
            for path in json_handler.loader(PATH_FILE):
                lats: list = path["lat"]
                lngs: list = path["lng"]
                route: int = int(path["RouteId"])
                var: int = int(path["RouteVarId"])
                path_list[(route, var)] = Path(PathData(lngs, lats, route, var))
                add_path_to_route(route, var, path_list[(route, var)])

            self._data = path_list
        return self.data


class PathHandler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PathHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.loader = PathLoader()

    def load(self):
        self.loader.load()

    @property
    def path_list(self) -> dict[tuple[int, int], Path]:
        return self.loader.load()

    def get_path_list(self) -> dict[tuple[int, int], Path]:
        return self.path_list

    def get_path_of_route_var(self, route: int, var: int) -> Path:
        return self.path_list[(route, var)]
