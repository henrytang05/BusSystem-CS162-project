import heapq
import os
import csv
from .Edge import Edge
from .Stop import StopHandler
from .RouteVar import RouteVarHandler
from .Path import PathHandler
from typing import Generator
import pandas as pd
from ..utils.helpers import ensure_path_exists, timeit


class Graph:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Graph, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, "vertices") or not hasattr(self, "short_paths"):
            self.vertices: dict[int, list[Edge]] = {}
            self.short_paths = {}
            self.make_graph()

    def ensure_data_loaded(self):
        RouteVarHandler().load()
        StopHandler().load()
        PathHandler().load()

    def make_graph(self):
        rv = RouteVarHandler()
        self.ensure_data_loaded()

        for route in rv.get_route_list().values():
            for var in route.vars.values():
                path = var.get_paths()
                for segment in path:
                    self.add_edge(
                        segment.start.StopId,
                        segment.end.StopId,
                        segment.time,
                        (var.routeid, var.varid),
                        segment.path,
                    )
        for stop in StopHandler().get_stops().keys():
            if stop not in self.vertices:
                self.vertices[stop] = []

    def add_edge(
        self,
        src: int,
        dest: int,
        time: float,
        routevar: tuple[int, int],
        path: list[tuple[float, float]],
    ):
        if src not in self.vertices:
            self.vertices[src] = []
        self.vertices[src].append(Edge(src, dest, time, routevar, path))

    @timeit
    def Dijkstra(
        self, start: int, target=None
    ) -> tuple[int, dict, dict[int, tuple[list[tuple[float, float]], int]]]:
        cost = {node: float("inf") for node in self.vertices}
        cost[start] = 0
        visited = set()
        prev = {node: -1 for node in self.vertices}
        path: dict[int, tuple[list[tuple[float, float]], int]] = {
            node: ([], -1) for node in self.vertices
        }
        path_count = {node: 0 for node in self.vertices}
        path_count[start] = 1

        pq: list[tuple[float, int]] = [(0, start)]
        while pq:
            current_cost, current_node = heapq.heappop(pq)
            if current_node == target:
                return (start, cost, path)
            if cost[current_node] < current_cost:
                continue
            visited.add(current_node)
            for edge in self.vertices[current_node]:
                if edge.dest in visited:
                    continue
                new_cost = current_cost + edge.time
                if new_cost < cost[edge.dest]:
                    cost[edge.dest] = new_cost
                    path_count[edge.dest] = path_count[current_node]
                    path.update({edge.dest: (edge.path, current_node)})
                    prev.update({edge.dest: current_node})
                    heapq.heappush(pq, (new_cost, edge.dest))
                elif new_cost == cost[edge.dest]:
                    path_count[edge.dest] += path_count[current_node]
        return (start, cost, path)

    def Dijkstra_all_pairs(
        self,
    ) -> Generator[
        tuple[int, dict, dict[int, tuple[list[tuple[float, float]], int]]], None, None
    ]:
        for src in self.vertices.keys():
            yield (self.Dijkstra(src))


def backtrack_path(
    path: dict[int, tuple[list[tuple[float, float]], int]], target: int
) -> list[tuple[float, float]]:

    result: list[tuple[float, float]] = []
    while target != -1:
        tmp = path[target][0]
        tmp.reverse()
        result += tmp
        target = path[target][1]

    result.reverse()

    return result


@ensure_path_exists("output/shortest_path")
def output_to_csv(result: tuple):
    src, cost, path = result
    data = [
        (src, des, timecost, backtrack_path(path, des))
        for des, timecost in cost.items()
    ]
    df = pd.DataFrame(data, columns=["src", "des", "time", "path"])
    CWD = os.getcwd()
    df.to_csv(
        f"{CWD}/output/shortest_path/{src}.csv",
        index=False,
        quoting=csv.QUOTE_NONNUMERIC,
        encoding="utf-8",
        mode="a",
    )
