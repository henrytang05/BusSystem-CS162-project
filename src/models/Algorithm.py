import asyncio
import heapq
from functools import partial
import pandas as pd
from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor
import os
import csv


def timeit(func):
    import time

    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter() - start} seconds")
        return result

    return wrapper


def Dijkstra(graph, start: int, target=None) -> tuple[dict, dict]:
    cost = {node: float("inf") for node in graph.vertices}
    cost[start] = 0
    visited = set()
    prev = {node: -1 for node in graph.vertices}
    path_count = {node: 0 for node in graph.vertices}
    path_count[start] = 1

    pq: list[tuple[float, int]] = [(0, start)]
    while pq:
        current_cost, current_node = heapq.heappop(pq)
        if current_node == target:
            return cost, prev
        if cost[current_node] < current_cost:
            continue
        visited.add(current_node)
        for edge in graph.vertices[current_node]:
            if edge.dest in visited:
                continue
            new_cost = current_cost + edge.time
            if new_cost < cost[edge.dest]:
                cost[edge.dest] = new_cost
                path_count[edge.dest] = path_count[current_node]
                heapq.heappush(pq, (new_cost, edge.dest))
                prev.update({edge.dest: current_node})
            elif new_cost == cost[edge.dest]:
                path_count[edge.dest] += path_count[current_node]
    return (cost, prev)


def backtrack_path(prev, target):
    path = []
    while target != -1:
        path.append(target)
        target = prev[target]
    return path[::-1]


@timeit
def Dijkstra_all_pairs(graph) -> dict[int, tuple[dict[int, float], dict[int, int]]]:
    """Run Dijkstra algorithm on all pairs"""
    result = {}
    for node in graph.nodes:
        cost, prev = Dijkstra(graph, node)
        result[node] = (cost, prev)
    return result


async def Dijkstra_all_pairs_multiprocessing(graph):

    nodes = graph.vertices
    partial_Dijkstra = partial(Dijkstra, graph)
    tasks = []
    with Pool() as pool:
        results = pool.imap_unordered(partial_Dijkstra, nodes)
        for res in zip(nodes, results):
            src, (cost, prev) = res
            tasks.append(asyncio.create_task(write_result_to_csv(src, cost, prev)))
    for task in tasks:
        await task


async def write_result_to_csv(src, cost, prev):
    data = [
        (src, des, time_cost, backtrack_path(prev, des))
        for des, time_cost in cost.items()
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
