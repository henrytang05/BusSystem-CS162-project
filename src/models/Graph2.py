import heapq
from ..utils.Cache import Cache
from ..utils.constants import ROUTEVAR_STOP_MAP, VAR_LIST, STOP_LIST


class Edge:
    def __init__(self, src: int, dest: int, time: float):
        self.src = src
        self.dest = dest
        self.time = time
        self.path = {}


class Graph:
    def __init__(self):
        self.vertices: dict[int, list[Edge]] = {}
        rtm = Cache.get(ROUTEVAR_STOP_MAP)
        routevar = Cache.get(VAR_LIST)
        for route, stops in rtm.items():
            ave_speed = routevar[route].Distance / (60 * routevar[route].RunningTime)
            # TODO: calculate tiem and distance
            import random

            distance = random.randint(1, 1000)

            prev_stop = stops[0]
            for stop in stops[1:]:
                if stop not in self.vertices:
                    self.vertices[stop] = []
                self.add_edge(prev_stop, stop, distance / ave_speed)
                prev_stop = stop

    def add_edge(self, src: int, dest: int, time: float):
        if src not in self.vertices:
            self.vertices[src] = []
        self.vertices[src].append(Edge(src, dest, time))

    def Dijkstra(self, start: int):
        Time = {node: float("inf") for node in self.vertices}
        Time[start] = 0

        cntPrev = {node: 0 for node in self.vertices}
        path = {}

        for node in self.vertices:
            path[node] = []

        pq = [(0, start)]

        cntPrev[start] = 1

        while pq:
            current_distance, current_vertex = heapq.heappop(pq)

            if current_distance > Time[current_vertex]:
                continue

            for edge in self.vertices[current_vertex]:
                TimeCost = current_distance + edge.time

                if TimeCost < Time[edge.dest]:
                    Time[edge.dest] = TimeCost
                    heapq.heappush(pq, (TimeCost, edge.dest))
                    cntPrev[edge.dest] = cntPrev[current_vertex]
                    path[edge.dest] = [edge.path, current_vertex]
                elif TimeCost == Time[edge.dest]:
                    cntPrev[edge.dest] += cntPrev[current_vertex]

        return Time

    def find_shortest_path(self):
        stops = Cache.get(STOP_LIST)
        results = []
        for stop in stops:
            results.append({stop: self.Dijkstra(stop)})

        return results

    def output_as_json(self, results: list):
        import json

        with open("output.json", "w") as f:
            json.dump(results, f)

    def print_results(self, results: list):
        for result in results:
            for src, (des, time) in result.items():
                print(f"From {src} to {des} {time} seconds")
