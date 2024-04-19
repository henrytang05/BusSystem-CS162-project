__all__ = ["Stop", "StopData", "StopLoader", "StopHandler"]

from dataclasses import dataclass
from ..utils import json_handler
from ..utils.constants import STOP_FILE
from .RouteVar import RouteVarHandler


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

    @property
    def id(self):
        return self.data.StopId

    @property
    def data(self) -> StopData:
        return self._data

    @data.setter
    def data(self, value: StopData):
        self._data = value

    def add_route(self, routeid):
        self.routes = map(int, self.data.Routes.split(", "))


class StopLoader:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StopLoader, cls).__new__(cls)
            cls._instance.load()
        return cls._instance

    def load(self) -> dict[int, Stop]:
        if self.stop_list:
            return self.stop_list

        self.stop_list: dict[int, Stop] = {}  # key: StopId, value: Stop
        _route_var_handler = RouteVarHandler()

        def add_to_route(routeid: int, varid: int, stop: Stop) -> None:
            _route_var_handler.get_var(routeid, varid).add_stop(stop)

        def add_to_stop_list(stop: dict) -> None:
            id: int = int(stop["StopId"])
            if id not in self.stop_list.keys():
                self.stop_list.update({id: Stop(StopData(**stop))})
            stop_object = self.stop_list.get(id)
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
        return self.stop_list


class StopHandler:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def stop_list(self) -> dict[int, Stop]:
        if not self._stop_list:
            self._stop_list: dict[int, Stop] = self.loader.load()
        return self._stop_list

    @property
    def loader(self) -> StopLoader:
        self._loader: StopLoader = StopLoader()
        return self._loader

    def get_stop(self, id: int) -> Stop:
        stop = self.stop_list.get(id)
        if not stop:
            raise ValueError(f"Stop with id {id} not found")
        return stop

    def get_stops(self) -> dict[int, Stop]:
        return self.stop_list
