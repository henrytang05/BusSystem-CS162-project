import heapq

from ..utils.Cache import Cache
from ..utils.constants import PATH_LIST, ROUTEVAR_STOP_MAP, STOP_LIST, VAR_LIST
from ..utils.helpers import calculate_distance, distance_finder, stop_finder
from .Edge import Edge
from geojson import LineString


class Graph:
    def __init__(self):
        self.vertices: dict[int, list[Edge]] = {}
        self.short_paths = {}
        rtm = Cache.get(ROUTEVAR_STOP_MAP)
        routevars = Cache.get(VAR_LIST)
        for routevar, stops in rtm.items():
            ave_speed = routevars[routevar].Distance / (
                60 * routevars[routevar].RunningTime
            )
            prev_stop = stops[0]
            df = distance_finder(routevar)
            for stop in stops[1:]:
                distance, path = df(prev_stop, stop)
                self.add_edge(prev_stop, stop, distance / ave_speed, routevar, path)
                prev_stop = stop

        for stopid, _ in Cache.get(STOP_LIST).items():
            if stopid not in self.vertices:
                self.vertices[stopid] = []

    def add_edge(
        self,
        src: int,
        dest: int,
        time: float,
        routevar: tuple[int, int],
        path: tuple[int, int],
    ):
        if src not in self.vertices:
            self.vertices[src] = []
        self.vertices[src].append(Edge(src, dest, time, routevar, path))

    def Dijkstra(self, start: int, target=None) -> tuple[dict, dict[int, list[Edge]]]:
        cost = {node: float("inf") for node in self.vertices}
        cost[start] = 0
        visited = set()
        path = {node: [] for node in self.vertices}
        path_count = {node: 0 for node in self.vertices}
        path_count[start] = 1

        pq: list[tuple[float, int]] = [(0, start)]
        while pq:
            current_cost, current_node = heapq.heappop(pq)
            if current_node == target:
                return cost, path
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
                    heapq.heappush(pq, (new_cost, edge.dest))
                    path[edge.dest].append(edge)
                elif new_cost == cost[edge.dest]:
                    path_count[edge.dest] += path_count[current_node]
        return (cost, path)

    def find_shortest_paths(self):
        stops = Cache.get(STOP_LIST)
        results = {}
        for stop in stops:
            cost, path = self.Dijkstra(stop)
            results[stop] = (cost, path)
            # self.output_as_json(cost)
            # del res
        self.short_paths = results
        return results

    def export_path(self, start: int, end: int):
        cost, path1 = self.Dijkstra(start, end)
        self.short_paths[start] = (cost, path1)
        time = self.short_paths[start][0][end]
        path = self.short_paths[start][1][end]

        if time == float("inf"):
            raise ValueError("There is no path")
        paths = Cache.get(PATH_LIST)
        line = []

        for edge in path:
            line += paths[edge.routevar].lng_lat_list[edge.path[0] : edge.path[1]]

        linestring = LineString(line)
        print(f"From {start} to {end} takes {time}")

        with open(f"shortest_paths/{start}_to_{end}.geojson", "w") as f:
            f.write(str(linestring))

    def output_as_json(self, result):
        import json

        with open("output.geojson", "a") as f:
            f.write(json.dumps(result, indent=4))
            f.write("\n")

    def print_results(self, results: list):
        for result in results:
            for src, (des, time) in result.items():
                print(f"From {src} to {des} {time} seconds")
