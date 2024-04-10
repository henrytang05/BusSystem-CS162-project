__all__ = ["Graph"]
from .Stop import Stop
from ..utils.Cache import Cache
from ..utils.json_handler import writer
from .RouteVar import RouteVar

import heapq
from ..utils.constants import *
from pyproj import Proj, CRS, Geod
from pqdict import pqdict


class Edge:
    def __init__(
        self,
        routevar: tuple[int, int],
        source: int,
        destination: int,
        time: float,
        distance: float,
    ):
        self.routevar = routevar
        self.source = source
        self.destination = destination
        self.time = time
        self.distance = distance

    def __repr__(self) -> str:
        return f"Edge:in ( {self.routevar[0]}, {self.routevar[1]} ), From {self.source}, to {self.destination}, {self.time}"

    def __str__(self) -> str:
        return f"Edge:in ( {self.routevar[0]}, {self.routevar[1]} ), From {self.source}, to {self.destination}, {self.time}"


class Graph:
    """A class to represent a Graph object"""

    graph: dict[int, list[Edge]] = {}

    def __new__(cls):
        if not cls.graph:
            crs = CRS.from_epsg(3405)
            proj = Proj(crs)

            for (routeid, varid), stopids in Cache.get(ROUTEVAR_STOP_MAP).items():
                routevar = Cache.get(VAR_LIST)[(routeid, varid)]
                average_velocity = routevar.Distance / (60 * routevar.RunningTime)
                last = Cache.get(STOP_LIST)[stopids[0]]
                assert len(stopids) > 1
                for stopid in stopids[1:]:
                    stop = Cache.get(STOP_LIST)[stopid]
                    last_x, last_y = proj(last.Lng, last.Lat)
                    stop_x, stop_y = proj(stop.Lng, stop.Lat)
                    distance = ((last_x - stop_x) ** 2 + (last_y - stop_y) ** 2) ** (
                        1 / 2
                    )
                    time = distance / average_velocity
                    if not cls.graph.get(last.StopId):
                        cls.graph[last.StopId] = []
                    cls.graph[last.StopId].append(
                        Edge((routeid, varid), last.StopId, stopid, time, distance)
                    )
                    last = stop

        return super().__new__(cls)

    def dijkstra(self, source, target=None):
        dist = {}
        pred = {}

        pq = pqdict.minpq()
        for node in self.graph:
            if node == source:
                pq[node] = 0
            else:
                pq[node] = float("inf")

        for node, min_dist in pq.popitems():
            dist[node] = min_dist
            if node == target:
                break

            for edge in self.graph[node]:
                if edge.destination in pq:
                    new_score = dist[node] + edge.time
                    if new_score < pq[edge.destination]:
                        pq[edge.destination] = new_score
                        pred[edge.destination] = node

        return dist, pred

    def find_all_shortest_paths(self):
        for src in self.graph.keys():
            if not Cache.get(SHORTEST_PATHS):
                Cache.add(SHORTEST_PATHS, {})
            dist, pred = self.dijkstra(src)
            for to, time in dist.items():
                if to != src:
                    Cache.get(SHORTEST_PATHS)[(src, to)] = time
            self.output_as_json()
            Cache.remove(SHORTEST_PATHS)

    def output_as_json(self):
        result = Cache.get(SHORTEST_PATHS)
        # for (stop, destination), time in result.items():
        #     print(f"From {stop.StopId} to {destination.StopId} in {time} second")
        data = [
            {"From": stop, "To": destination, "Take": time}
            for (stop, destination), time in result.items()
        ]
        import json

        with open("shortest.json", "w") as file:
            json.dump(data, file)
            file.write("\n")

        # with open("shortest.json", "w") as file:
        #     for item in data:
        #         json.dump(item, file)
        #         file.write("\n")
