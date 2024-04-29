import heapq
import time
import os
import csv
from .Edge import Edge
from .Stop import StopHandler
from .RouteVar import RouteVarHandler
from .Path import PathHandler
import pandas as pd


class Graph:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Graph, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, "vertices") or not hasattr(self, "short_paths"):
            self.vertices = {}
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

    # def output_result_to_csv(self):
    #     io_time = 0
    #
    #     for result in self.find_shortest_paths():
    #
    #         start = time.time()
    #         src = result[0]
    #         cost = result[1]
    #         path = result[2]
    #         data = [
    #             (src, des, time, self.backtrack_path(path, des))
    #             for des, time in cost.items()
    #         ]
    #
    #         import os
    #         import csv
    #
    #         df = pd.DataFrame(data, columns=["src", "des", "time", "path"])
    #         CWD = os.getcwd()
    #         df.to_csv(
    #             f"{CWD}/output/shortest_path/{src}.csv",
    #             index=False,
    #             quoting=csv.QUOTE_NONNUMERIC,
    #             encoding="utf-8",
    #             mode="a",
    #         )
    #         end = time.time()
    #         io_time += end - start
    #
    #     print("Total I/O time:", io_time, "seconds")

    # def output_result_to_csv_multiprocess(self):
    #     sh = StopHandler().get_stops()
    #
    #     stops = [stop for stop in sh]
    #     with concurrent.futures.ProcessPoolExecutor() as executor:
    #         executor.map(wrapped, stops)
    # for result in results:
    #     src = result[0]
    #     cost = result[1]
    #     path = result[2]
    #     data = [
    #         (src, des, time, backtrack_path(path, des))
    #         for des, time in cost.items()
    #     ]
    #     df = pd.DataFrame(data, columns=["src", "des", "time", "path"])
    #     CWD = os.getcwd()
    #     df.to_csv(
    #         f"{CWD}/output/shortest_path/{src}.csv",
    #         index=False,
    #         quoting=csv.QUOTE_NONNUMERIC,
    #         encoding="utf-8",
    #         mode="a",
    #     )


def backtrack_path(path: dict, target: int) -> list:
    result = []
    if path[target] == -1:
        return result
    while target != -1:
        result.append(target)
        target = path[target]
    result.reverse()

    return result


# def find_shortest_path_from():
graph = Graph()


def wrapped(src: int):
    global graph
    start = time.time()
    cost, path = graph.Dijkstra(src)
    end = time.time()
    print("From", src, ":", end - start, "seconds")
    output_to_csv(src, cost, path)
    # return (src, cost, path)


def output_to_csv(src, cost, path):
    data = [(src, des, time, backtrack_path(path, des)) for des, time in cost.items()]
    df = pd.DataFrame(data, columns=["src", "des", "time", "path"])
    CWD = os.getcwd()
    df.to_csv(
        f"{CWD}/output/shortest_path/{src}.csv",
        index=False,
        quoting=csv.QUOTE_NONNUMERIC,
        encoding="utf-8",
        mode="a",
    )
