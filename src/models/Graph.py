import heapq

from ..utils.Cache import Cache
from ..utils.constants import PATH_LIST, ROUTEVAR_STOP_MAP, STOP_LIST, VAR_LIST
from ..utils.helpers import calculate_distance
from .Path import Path
from pyproj import Geod


class Edge:
    def __init__(self, src: int, dest: int, time: float):
        self.src = src
        self.dest = dest
        self.time = time
        self.path: list[Path] = []


def distance_finder(routevar):
    pf = path_finder(routevar)

    def find_distance(stop1, stop2):
        stops = Cache.get(STOP_LIST)
        lng1 = stops[stop1].Lng
        lat1 = stops[stop1].Lat
        lng2 = stops[stop2].Lng
        lat2 = stops[stop2].Lat

        index1: int = pf((lng1, lat1))
        index2: int = pf((lng2, lat2))
        path = Cache.get(PATH_LIST)[routevar]
        assert index1 >= 0 and index1 < len(path.lng_lat_list)
        assert index2 >= 0 and index2 < len(path.lng_lat_list)

        lngs = path.lngs[index1:index2]
        lats = path.lats[index1:index2]
        geo = Geod(ellps="WGS84")
        return geo.line_length(lngs, lats)

    return find_distance


def path_finder(routevar):
    last_found = 0
    path = Cache.get(PATH_LIST)[routevar]

    def find(stop: tuple[float, float]) -> int:
        nonlocal last_found
        closest_dis = float("inf")
        for i in range(last_found, len(path.lng_lat_list)):
            loc = path.lng_lat_list[i]
            distance = calculate_distance(loc, stop)
            if distance < closest_dis:
                last_found = i
                closest_dis = distance
        return last_found

    return find


class Graph:
    def __init__(self):
        self.vertices: dict[int, list[Edge]] = {}
        rtm = Cache.get(ROUTEVAR_STOP_MAP)
        routevar = Cache.get(VAR_LIST)
        for route, stops in rtm.items():
            ave_speed = routevar[route].Distance / (60 * routevar[route].RunningTime)
            prev_stop = stops[0]
            df = distance_finder(route)
            for stop in stops[1:]:
                distance = df(prev_stop, stop)
                self.add_edge(prev_stop, stop, distance / ave_speed)
                prev_stop = stop

        for stopid, _ in Cache.get(STOP_LIST).items():
            if stopid not in self.vertices:
                self.vertices[stopid] = []

    def add_edge(self, src: int, dest: int, time: float):
        if src not in self.vertices:
            self.vertices[src] = []
        self.vertices[src].append(Edge(src, dest, time))

    def Dijkstra(self, start: int) -> dict:
        cost = {node: float("inf") for node in self.vertices}
        cost[start] = 0
        visited = set()

        pq: list[tuple[float, int]] = [(0, start)]
        while pq:
            current_cost, current_node = heapq.heappop(pq)
            if cost[current_node] < current_cost:
                continue
            visited.add(current_node)
            for edge in self.vertices[current_node]:
                if edge.dest in visited:
                    continue
                new_cost = current_cost + edge.time
                if new_cost < cost[edge.dest]:
                    cost[edge.dest] = new_cost
                    heapq.heappush(pq, (new_cost, edge.dest))
        return cost

    def find_shortest_path(self):
        stops = Cache.get(STOP_LIST)
        # results = []
        for stop in stops:
            res = self.Dijkstra(stop)
            # results.append({stop: res})
            self.output_as_json(res)
            del res

        # return results

    def output_as_json(self, result):
        import json

        with open("output.json", "a") as f:
            f.write(json.dumps(result, indent=4))
            f.write("\n")

    def print_results(self, results: list):
        for result in results:
            for src, (des, time) in result.items():
                print(f"From {src} to {des} {time} seconds")
