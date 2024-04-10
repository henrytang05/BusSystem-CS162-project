__all__ = ["Stop"]
from dataclasses import dataclass
from ..utils import json_handler
from ..utils.Cache import Cache
from ..utils.constants import STOP_FILE, STOP_LIST, ROUTEVAR_STOP_MAP, VAR_LIST
from .RouteVar import RouteVar
from .RouteVarQuery import RouteVarQuery
from ..utils.helpers import intersection


@dataclass(frozen=True)
class Stop:
    """A data class to represent a Stop object"""

    StopId: int
    Code: str
    Name: str
    StopType: str
    Zone: str
    Ward: str
    AddressNo: str
    Street: str
    SupportDisability: str
    Status: str
    Lng: float
    Lat: float
    Search: str
    Routes: str

    @classmethod
    def load_stop(cls) -> list:
        """Load from STOPFILE and cache it"""
        if not Cache.get(VAR_LIST):
            RouteVar.load_route_var()
        if not Cache.get(STOP_LIST):
            stop_list: dict[int, Stop] = {}
            route_stop_map: dict[tuple[int, int], list[int]] = {}
            for obj in json_handler.loader(STOP_FILE):
                stops: list = obj["Stops"]
                varid: int = int(obj["RouteVarId"])
                routeid: int = int(obj["RouteId"])
                for stop in stops:
                    if not stop_list.get(stop["StopId"]):
                        stop_object = Stop(**stop)
                        stop_list[stop["StopId"]] = stop_object
                    if (routeid, varid) not in route_stop_map:
                        route_stop_map[(routeid, varid)] = []
                    route_stop_map[(routeid, varid)].append(stop["StopId"])
            Cache.add(STOP_LIST, stop_list)
            Cache.add(ROUTEVAR_STOP_MAP, route_stop_map)
        return Cache.get(STOP_LIST)
