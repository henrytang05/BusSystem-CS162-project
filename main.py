from src.models.Graph import Graph
import time


def graph():

    g = Graph()
    start = time.time()
    g.output_result_to_csv_multiprocess()
    end = time.time()
    print("Total time:", end - start, "seconds")


def main():
    graph()


if __name__ == "__main__":
    main()
