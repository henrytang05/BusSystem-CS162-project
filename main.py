from src.models.Graph import Graph
from src.models.Algorithm import Dijkstra_all_pairs_multiprocessing
import asyncio
import time


def graph():

    g = Graph()
    start = time.time()
    asyncio.run(Dijkstra_all_pairs_multiprocessing(g))
    end = time.time()
    print("Total time:", end - start, "seconds")


def main():
    graph()


if __name__ == "__main__":
    main()
