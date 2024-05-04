import time
import asyncio
from concurrent.futures import ProcessPoolExecutor

from src.models.Graph import Graph, output_to_csv


def graph():
    g = Graph()
    start = time.time()
    num_processes = 7  # Specify the number of processes here
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        for res in g.Dijkstra_all_pairs():
            res = tuple(res)
            executor.submit(output_to_csv, res)

    end = time.time()
    print("Total time:", end - start, "seconds")


def main():
    graph()


if __name__ == "__main__":
    main()
