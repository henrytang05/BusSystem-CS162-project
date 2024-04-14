__all__ = ["Path"]

from dataclasses import dataclass
from ..utils import json_handler
from ..utils.Cache import Cache
from ..utils.constants import PATH_FILE, PATH_LIST


@dataclass
class Path:
    """A data class to represent a Path object"""

    lng_lat_list: list[tuple]
    lngs: list[float]
    lats: list[float]
    RouteId: int
    RouteVarId: int

    @classmethod
    def load_path(cls) -> list | None:
        """Load the from the VAR_FILE file and cache it"""
        if not Cache.get(PATH_LIST):
            path_list: dict[tuple[int, int], Path] = {}
            for path in json_handler.loader(PATH_FILE):
                lats: list = path["lat"]
                lngs: list = path["lng"]
                route: int = int(path["RouteId"])
                var: int = int(path["RouteVarId"])
                lng_lat_list: list[tuple] = list(zip(lngs, lats))
                path_list[(route, var)] = Path(lng_lat_list, lngs, lats, route, var)

            Cache.add(PATH_LIST, path_list)
        return Cache.get(PATH_LIST)
