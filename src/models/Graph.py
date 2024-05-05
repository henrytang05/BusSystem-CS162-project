import heapq
import os
import csv
from .StopQuery import StopQuery
from .Edge import Edge
from .Stop import StopHandler
from .RouteVar import RouteVarHandler
from .Path import PathHandler
from typing import Generator
import pandas as pd
from ..utils.helpers import ensure_path_exists, timeit


class DijkstraResult:
    def __init__(
        self,
        start: int,
        cost: dict[int, float],
        paths: dict[int, tuple[Edge, int]],
        time_m_to_n: list[dict],
        max_time: float,
        min_time: float,
        avg_time: float,
        stop_importance_time: float,
        target=None,
    ):
        self.start = start
        self.target = target
        self.cost = cost
        self.paths_not_backtracked = paths
        self.max_time = max_time
        self.min_time = min_time
        self.avg_time = avg_time
        self.stop_importance_time = stop_importance_time
        self.time_record = time_m_to_n

    @property
    def paths(self):
        if not hasattr(self, "_paths"):
            self._paths = self.backtrack_all_path(self.paths_not_backtracked)
        return self._paths

    def backtrack_all_path(self, paths) -> dict[int, list[Edge]]:
        result = {}
        for target in self.cost.keys():
            result[target] = self.backtrack_path(paths, target)
        return result

    def backtrack_path(
        self, paths: dict[int, tuple[Edge, int]], target: int
    ) -> list[Edge]:

        if target not in paths.keys():
            return []
        at = target
        result: list[Edge] = []
        while at is not None:
            result.append(paths[at][0])
            at = paths[at][1]

        result.pop()
        result.reverse()

        return result

    def convert_to_geojson(self):
        co = []
        co_var = []
        if self.target is not None:
            for edge in self.paths[self.target]:
                co.extend(edge.convert_to_geojson())
                co_var.extend(edge.convert_var_to_geojson())
            return co, co_var

        for _, path in self.paths.items():
            for edge in path:
                co.extend(edge.convert_to_geojson())
                co_var.extend(edge.convert_var_to_geojson())
        return co, co_var

    @ensure_path_exists("output/")
    def output_to_csv(self):
        data = [(self.start, des, timecost) for des, timecost in self.cost.items()]
        df = pd.DataFrame(
            data,
            columns=["src", "des", "time"],
        )
        CWD = os.getcwd()
        df.to_csv(
            f"{CWD}/output/allpairs.csv",
            index=False,
            quoting=csv.QUOTE_NONNUMERIC,
            encoding="utf-8",
            mode="a",
        )


def ensure_data_loaded(func):
    def wrapped(*args, **kwargs):
        RouteVarHandler().load()
        StopHandler().load()
        PathHandler().load()
        return func(*args, **kwargs)

    return wrapped


class Graph:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Graph, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, "vertices") or not hasattr(self, "short_paths"):
            self.vertices: dict[int, list[Edge]] = {}
            self.stop_priority = {}
            self.make_graph()

    @ensure_data_loaded
    def make_graph(self):
        rv = RouteVarHandler()

        for route in rv.get_route_list().values():
            for var in route.vars.values():
                path = var.get_paths()
                for segment in path:
                    self.add_edge(
                        Edge(
                            segment.start,
                            segment.end,
                            segment.time,
                            segment.path,
                            var,
                        )
                    )
        for stop in StopHandler().get_stops().keys():
            if stop not in self.vertices:
                self.vertices[stop] = []

    def add_edge(self, edge: Edge):
        if edge.src not in self.vertices:
            self.vertices[edge.src] = []
        self.vertices[edge.src].append(edge)

    @timeit
    def Dijkstra(self, start: int, target=None) -> DijkstraResult:
        import time

        beginning = time.perf_counter()
        time_from_src_to_n = {node: float("inf") for node in self.vertices}
        time_from_src_to_n[start] = 0
        cost = {node: float("inf") for node in self.vertices}
        cost[start] = 0
        visited = set()
        path = {}  # {to : (edge, from)}
        path[start] = (None, None)
        cntFirst: dict[int, int] = {node: 0 for node in self.vertices}
        cntFirst[start] = 1

        pq: list[tuple[float, int]] = [(0, start)]
        while pq:
            current_cost, current_node = heapq.heappop(pq)
            if current_node == target:

                time_from_n_to_m = [
                    {"from": start, "to": to, "time": time_taken}
                    for to, time_taken in time_from_src_to_n.items()
                ]
                return DijkstraResult(
                    start,
                    cost,
                    path,
                    time_from_n_to_m,
                    max(time_from_src_to_n.values()),
                    min(time_from_src_to_n.values()),
                    sum(time_from_src_to_n.values()) / len(time_from_src_to_n),
                    time.perf_counter() - beginning,
                    target,
                )
            if cost[current_node] < current_cost:
                continue
            visited.add(current_node)
            for edge in self.vertices[current_node]:
                if edge.dest in visited:
                    continue
                new_cost = current_cost + edge.time
                if new_cost < cost[edge.dest]:
                    now = time.perf_counter()
                    if now - beginning < time_from_src_to_n[edge.dest]:
                        time_from_src_to_n[edge.dest] = now - beginning
                    cost[edge.dest] = new_cost
                    cntFirst[edge.dest] = cntFirst[current_node]
                    path.update({edge.dest: (edge, current_node)})
                    heapq.heappush(pq, (new_cost, edge.dest))
                elif new_cost == cost[edge.dest]:
                    cntFirst[edge.dest] += cntFirst[current_node]

        list_nodes = sorted(
            [(stop, val) for stop, val in cost.items()],
            key=lambda x: x[1],
            reverse=True,
        )
        cntSecond = {node: 0 for node in self.vertices}
        for u, val in list_nodes:
            if val == float("inf"):
                continue

            for edge in self.vertices[u]:
                v = edge.dest
                if cost[v] == cost[u] + edge.time:
                    cntSecond[u] += cntSecond[v]
            cntSecond[u] += 1
        for n, v in cost.items():
            if v == float("inf"):
                continue
            self.stop_priority[n] += cntSecond[n] * cntFirst[n]
        time_from_n_to_m = [
            {"from": start, "to": to, "time": time_taken}
            for to, time_taken in time_from_src_to_n.items()
        ]
        valid_time_stamp = [
            tm for tm in time_from_src_to_n.values() if tm != float("inf")
        ]
        end = time.perf_counter()
        stop_importance_time = end - beginning
        return DijkstraResult(
            start,
            cost,
            path,
            time_from_n_to_m,
            max(valid_time_stamp),
            min(valid_time_stamp),
            sum(valid_time_stamp) / len(valid_time_stamp),
            stop_importance_time,
            target,
        )

    def get_top_k_important_stops(self, k: int = 10):
        if not self.stop_priority:
            raise RuntimeError("Please run Dijkstra all pair first")
        list_priority = sorted(
            [x for x in self.stop_priority.items()], key=lambda x: x[1], reverse=True
        )
        result = []
        q = StopQuery()
        for cnt in list_priority[:k]:
            print(cnt[0], cnt[1])
            result.extend(q.search("StopId", cnt[0]))
        from ..utils import json_handler

        json_handler.writer("output/top_k_important.json", result)
        return result

    def Dijkstra_all_pairs(
        self,
    ) -> Generator[
        DijkstraResult,
        None,
        None,
    ]:
        self.stop_priority = {stop: 0 for stop in self.vertices.keys()}
        for src in self.vertices.keys():
            yield self.Dijkstra(src)

    @timeit
    def Dijkstra_all_pairs_and_record_csv(self):
        result = []
        for stop in self.vertices.keys():
            res = self.Dijkstra(stop)
            timecost = res.cost
            for des, time in timecost.items():
                result.append((stop, des, time))
        df = pd.DataFrame(
            result,
            columns=["src", "des", "time"],
        )
        CWD = os.getcwd()
        df.to_csv(
            f"{CWD}/output/allpairs.csv",
            index=False,
            quoting=csv.QUOTE_NONNUMERIC,
            encoding="utf-8",
            mode="w",
        )
