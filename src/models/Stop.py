from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .RouteVar import Var
__all__ = ["Stop", "StopData", "StopLoader", "StopHandler"]
from dataclasses import dataclass
from ..utils import json_handler
from ..utils.constants import STOP_FILE


@dataclass(frozen=True)
class StopData:
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


class Stop:

    def __init__(self, data: StopData):
        self.data = data
        self._vars = {}

    @property
    def id(self):
        return self.data.StopId

    @property
    def routes_no(self) -> list[str]:
        return [route for route in self.data.Routes.split(", ")]

    @property
    def vars(self) -> dict[int, Var]:
        return self._vars

    def add_var(self, var: Var) -> None:
        self.vars.update({var.varid: var})


class StopLoader:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StopLoader, cls).__new__(cls)
            # cls._instance.load()
        return cls._instance

    @property
    def data(self) -> dict[int, Stop]:
        if not hasattr(self, "_data"):
            self._data = {}
        return self._data

    def load(self) -> dict[int, Stop]:
        from .RouteVar import RouteVarHandler

        if self.data:
            return self.data
        _route_var_handler = RouteVarHandler()

        def add_to_route(routeid: int, varid: int, stop: Stop) -> None:
            _route_var_handler.get_var(routeid, varid).add_stop(stop)

        def add_to_stop_list(stop: dict) -> None:
            id: int = int(stop["StopId"])
            if id not in self.data.keys():
                self.data.update({id: Stop(StopData(**stop))})
            stop_object = self.data.get(id)
            assert isinstance(stop_object, Stop)
            add_to_route(routeid, varid, stop_object)

        for yielded_data in json_handler.loader(STOP_FILE):
            if not yielded_data:
                continue
            stops: list = yielded_data["Stops"]
            varid: int = int(yielded_data["RouteVarId"])
            routeid: int = int(yielded_data["RouteId"])
            for stop in stops:
                add_to_stop_list(stop)
        return self.data


class StopHandler:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(StopHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.loader = StopLoader()

    @property
    def stop_list(self) -> dict[int, Stop]:
        return self.loader.load()

    def get_stop(self, id: int) -> Stop:
        stop = self.stop_list.get(id)
        if not stop:
            raise ValueError(f"Stop with id {id} not found")
        return stop

    def get_stops(self) -> dict[int, Stop]:
        return self.stop_list

    def load(self) -> dict[int, Stop]:
        return self.loader.load()
