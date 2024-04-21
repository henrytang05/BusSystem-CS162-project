__all__ = ["VarData", "Var", "Route", "RouteVarLoader", "RouteVarHandler"]

from dataclasses import dataclass
from .RouteStop import RouteStop
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
        self.stop = {}

    def add_stop(self, stop: RouteStop) -> None:
        self.stops.update({stop.id: stop})
        stop.add_var(self)

    @property
    def stops(self) -> dict[int, RouteStop]:
        return self._stops

    @stops.setter
    def stops(self, value: dict[int, RouteStop]) -> None:
        self._stops = value

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

    def __init__(self, *vars: Var):
        self.vars = {}
        for var in vars:
            self.add_var(var)
        # self.vars = vars

    @property
    def vars(self) -> dict[int, Var]:
        return self._vars

    @vars.setter
    def vars(self, value: dict[int, Var]):
        self._vars = value

    # @vars.setter
    # def vars(self, value: tuple[Var, ...] | Var):
    #     if isinstance(value, tuple):
    #         self._vars: dict[int, Var] = {}
    #         for var in value:
    #             self._vars[var.id] = var
    #     elif isinstance(value, Var):
    #         self._vars = {value.id: value}
    #     else:
    #         raise ValueError(
    #             "Invalid input type for vars. Expected tuple[Var, ...] or Var."
    #         )

    @property
    def id(self) -> int:
        if self.vars:
            return self.vars[0].data.RouteId
        else:
            raise ValueError("Route has no vars")

    def get_vars(self) -> dict[int, Var]:
        return self.vars

    def add_var(self, var: Var) -> None:
        self.vars.update({var.id: var})

    def get_var(self, id: int) -> Var:
        var = self.vars.get(id, None)
        if not var:
            raise ValueError(f"Var with id {id} not found")
        return var


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
            self.data[id] = Route(*vars)

        return self.data


class RouteVarHandler:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.loader: RouteVarLoader = RouteVarLoader()
        self.route_list: dict[int, Route] = self.loader.load()

    def add_route(self, route: Route) -> None:
        self.route_list.update({route.id: route})

    def get_route(self, id: int) -> Route:
        for id, route in self.route_list.items():
            if route.id == id:
                return route
        raise ValueError(f"Route with id {id} not found")

    def get_var(self, routeid: int, varid: int) -> Var:
        route: Route = self.get_route(routeid)
        if not route:
            raise ValueError(f"Route with id {routeid} not found")
        return route.get_var(varid)

    def get_route_list(self) -> dict[int, Route]:
        return self.route_list
