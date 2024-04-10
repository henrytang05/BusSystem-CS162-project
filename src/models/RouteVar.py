__all__ = ["RouteVar"]

from dataclasses import dataclass
from ..utils import json_handler
from ..utils.Cache import Cache
from ..utils.constants import VAR_FILE, VAR_LIST


@dataclass(frozen=True)
class RouteVar:
    """A data class to represent a RouteVar object"""

    RouteId: int
    RouteVarId: int
    RouteVarName: str
    RouteVarShortName: str
    RouteNo: str
    StartStop: str
    EndStop: str
    Distance: float
    Outbound: bool
    RunningTime: float

    @classmethod
    def load_route_var(cls) -> list | None:
        """Load the from the VAR_FILE file and cache it"""
        if Cache.get(VAR_LIST):
            return Cache.get(VAR_LIST)

        route_var_list: dict[tuple[int, int], RouteVar] = {}
        for route_var in json_handler.loader(VAR_FILE):
            for var in route_var:
                route_var_list[(var["RouteId"], var["RouteVarId"])] = RouteVar(**var)

        Cache.add(VAR_LIST, route_var_list)
        return Cache.get(VAR_LIST)
