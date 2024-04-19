__all__ = ["VarData", "Var", "Route", "RouteVarLoader", "RouteVarHandler"]

from dataclasses import dataclass
from .Stop import Stop
from ..utils import json_handler

# from ..utils.Cache import Cache
from ..utils.constants import VAR_FILE


@dataclass(frozen=True)
class VarData:
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


class Var:
    def __init__(self, data: VarData):
        self.data = data
        self.stops: dict[int, Stop] = {}

    def add_stop(self, stop: Stop) -> None:
        self.stops.update({stop.id: stop})

    @property
    def id(self) -> int:
        return self.data.RouteVarId

    @property
    def data(self):
        """The data property."""
        return self._data

    @data.setter
    def data(self, value):
        self._data = value


class Route:
    """A data class to represent a Route object"""

    def __init__(self, id: int, *vars: Var):
        self.id = id
        self.vars: dict[int, Var] = {}
        for var in vars:
            self.vars[var.id] = var

    def get_vars(self) -> dict[int, Var]:
        return self.vars

    def add_var(self, var: Var) -> None:
        self.vars.update({var.id: var})

    def get_var(self, id: int) -> Var:
        var = self.vars.get(id, None)
        if not var:
            raise ValueError(f"Var with id {id} not found")
        return var

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        self._id = value


class RouteVarLoader:
    """A class to load the route_var data from the VAR_FILE file"""

    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load(self) -> dict[int, Route]:
        """Load the from the VAR_FILE file and cache it"""
        if self.data:
            return self.data

        self.data: dict[int, Route] = {}

        for route in json_handler.loader(VAR_FILE):
            if not route:
                continue
            id = route[0]["RouteId"]
            vars: list[Var] = [Var(VarData(**var)) for var in route]
            self.data[id] = Route(id, *vars)

        return self.data


class RouteVarHandler:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def loader(self) -> RouteVarLoader:
        if not self._loader:
            self._loader: RouteVarLoader = RouteVarLoader()
        return self._loader

    @property
    def route_list(self) -> dict[int, Route]:
        if not self._route_list:
            self._route_list: dict[int, Route] = self.loader.load()
        return self._route_list

    def add_route(self, route: Route) -> None:
        self.route_list.update({route.id: route})

    def get_route(self, id: int) -> Route:
        for id, route in self.route_list.items():
            if route.id == id:
                return route
        raise ValueError(f"Route with id {id} not found")

    def load_route(self) -> dict[int, Route]:
        return self.route_list

    def get_var(self, routeid: int, varid: int) -> Var:
        route: Route = self.get_route(routeid)
        if not route:
            raise ValueError(f"Route with id {routeid} not found")
        return route.get_var(varid)

    def get_route_list(self) -> dict[int, Route]:
        return self.route_list
