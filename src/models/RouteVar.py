from __future__ import annotations
from typing import TYPE_CHECKING
from rtree import index
from pyproj import Geod, Proj
from itertools import islice

if TYPE_CHECKING:
    from .Path import PathData
    from .Stop import Stop
__all__ = ["VarData", "Var", "Route", "RouteVarLoader", "RouteVarHandler"]

from dataclasses import dataclass

from .PathStop import PathStop
from ..utils import json_handler
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
        self.stops: list[Stop] = []
        self.path: list[PathStop] = []

    def add_stop(self, stop: Stop) -> None:
        self.stops.append(stop)
        stop.add_var(self)

    @property
    def varid(self) -> int:
        return self.data.RouteVarId

    @property
    def routeid(self) -> int:
        return self.data.RouteId

    def get_stops(self) -> list[Stop]:
        return self.stops

    def get_paths(self) -> list[PathStop]:
        return self.path

    def add_path(self, whole_path: PathData) -> None:

        lng_lat_list: list[tuple[float, float]] = list(
            zip(whole_path.lngs, whole_path.lats)
        )
        geo = Geod(ellps="WGS84")

        def finder():

            last_found_index = 0

            def find_closest_point(tar: tuple[float, float]) -> int:

                nonlocal last_found_index

                found = last_found_index
                best_dis = float("inf")
                for i, point in enumerate(lng_lat_list[last_found_index:]):
                    i += last_found_index
                    lngs = (point[0], tar[0])
                    lats = (point[1], tar[1])
                    this = geo.line_length(lngs, lats)
                    if this < best_dis:
                        best_dis = this
                        found = i

                if last_found_index > found:
                    raise ValueError("OMG what the heck")
                if not found:
                    raise ValueError("Something wrong when mapping into path")
                last_found_index = found
                return found

            return find_closest_point

        fd = finder()

        path_stop_list: list[PathStop] = []
        prev = self.stops[0].data
        last_found = 0
        velocity = self.data.Distance / (60 * self.data.RunningTime)
        for stop in self.stops[1:]:
            stop = stop.data
            this_found = fd((stop.Lng, stop.Lat))
            lngs = whole_path.lngs[last_found:this_found]
            lats = whole_path.lats[last_found:this_found]
            path: list[tuple[float, float]] = list(
                zip(
                    lngs,
                    lats,
                )
            )
            distance = geo.line_length(lngs, lats)
            time = distance / velocity
            path_stop_list.append(PathStop(prev, stop, distance, time, path))
            prev = stop
            last_found = this_found

        self.path = path_stop_list

    # def add_path(self, whole_path: PathData) -> None:
    #
    #     class Point:
    #         def __init__(self, x: float, y: float):
    #             self.x = x
    #             self.y = y
    #
    #     lng_lat_list: list[tuple[float, float]] = list(
    #         zip(whole_path.lngs, whole_path.lats)
    #     )
    #     proj = Proj("epsg:3405")
    #     lng_lat_in_xy: list[tuple[float, float]] = [
    #         proj(*point) for point in lng_lat_list
    #     ]
    #     geo = Geod(ellps="WGS84")
    #
    #     idx = index.Index()
    #     xy_points = [
    #         idx.insert(i, (*point, *point)) for i, point in enumerate(lng_lat_in_xy)
    #     ]
    #
    #     path_stop_list: list[PathStop] = []
    #     prev_stop = self.stops[0].data
    #     last_found = 0
    #     velocity = self.data.Distance / (60 * self.data.RunningTime)
    #     for this_stop in self.stops[1:]:
    #         this_stop = this_stop.data
    #
    #         stop_lng, stop_lat = this_stop.Lng, this_stop.Lat
    #         xy_point = proj(stop_lng, stop_lat)
    #         nearest_point_id = list(idx.nearest((*xy_point, *xy_point), 1))[0]
    #         this_found = nearest_point_id
    #         # assert this_found > last_found
    #         if this_found < last_found:
    #             print(
    #                 this_found,
    #                 last_found,
    #                 self.routeid,
    #                 self.varid,
    #                 this_stop.StopId,
    #                 prev_stop.StopId,
    #             )
    #         assert this_found < len(whole_path.lngs)
    #
    #         lngs = islice(whole_path.lngs, last_found, this_found)
    #         lats = islice(whole_path.lats, last_found, this_found)
    #         path: list[tuple[float, float]] = list(
    #             zip(
    #                 lngs,
    #                 lats,
    #             )
    #         )
    #         distance = geo.line_length(lngs, lats)
    #         time = distance / velocity
    #         path_stop_list.append(PathStop(prev_stop, this_stop, distance, time, path))
    #
    #         for j in range(last_found, this_found):
    #             idx.delete(j, (*lng_lat_in_xy[j], *lng_lat_in_xy[j]))
    #         prev_stop = this_stop
    #         last_found = this_found
    #
    #     self.path = path_stop_list

    def convert_to_geojson(self):
        from geojson import Point, LineString, Feature

        co = []
        for path in self.path:
            start = path.start
            sid = start.StopId
            end = path.end
            send = end.StopId
            road = path.path
            start = Point((start.Lng, start.Lat))
            end = Point((end.Lng, end.Lat))
            road = LineString(road)
            co.append(Feature(geometry=start, properties={"name": f"start {sid}"}))
            co.append(Feature(geometry=end, properties={"name": f"end {send}"}))
            co.append(
                Feature(
                    geometry=road,
                    properties={
                        "name": f"from {sid} to {send}",
                        "route": self.data.RouteId,
                        "var": self.data.RouteVarId,
                    },
                )
            )

        return co


class Route:
    """A data class to represent a Route object"""

    def __init__(self, *vars: Var):
        self.vars: dict[int, Var] = {}
        for var in vars:
            self.add_var(var)
        # self.vars = vars

    @property
    def id(self) -> int:
        if self.vars:
            return next(iter(self.vars.items()))[1].data.RouteId
        else:
            raise ValueError("Route has no vars")

    def get_vars(self) -> dict[int, Var]:
        return self.vars

    def add_var(self, var: Var) -> None:
        self.vars.update({var.varid: var})

    def get_var(self, id: int) -> Var:
        var = self.vars.get(id, None)
        if not var:
            raise ValueError(f"Var with id {id} not found")
        return var

    def convert_to_geojson(self) -> list:
        co = []
        for var in self.vars.values():
            co += var.convert_to_geojson()
        return co


class RouteVarLoader:
    """A class to load the route_var data from the VAR_FILE file"""

    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(RouteVarLoader, cls).__new__(cls)
        return cls._instance

    @property
    def data(self) -> dict[int, Route]:
        if not hasattr(self, "_data"):
            self._data = {}
        return self._data

    def load(self) -> dict[int, Route]:
        """Load the from the VAR_FILE file and cache it"""
        if self.data:
            return self.data

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
            cls._instance = super(RouteVarHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.loader = RouteVarLoader()

    @property
    def route_list(self) -> dict[int, Route]:
        return self.loader.load()

    def add_route(self, route: Route) -> None:
        self.route_list.update({route.id: route})

    def get_route(self, routeid: int) -> Route:
        for id, route in self.route_list.items():
            if id == routeid:
                return route
        raise ValueError(f"Route with id {routeid} not found")

    def get_var(self, routeid: int, varid: int) -> Var:
        route: Route = self.get_route(routeid)
        if not route:
            raise ValueError(f"Route with id {routeid} not found")
        return route.get_var(varid)

    def get_route_list(self) -> dict[int, Route]:
        return self.route_list

    def load(self) -> dict[int, Route]:
        return self.loader.load()
