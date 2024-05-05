from src.models.Graph import Graph


def output_all_pairs_Dijkstra():

    g = Graph()
    g.Dijkstra_all_pairs_and_record_csv()


def get_top_k_stop():
    g = Graph()
    import time

    st = time.perf_counter()
    for res in g.Dijkstra_all_pairs():
        pass
    et = time.perf_counter()
    print(f"Dijkstra all pairs time: {et-st}")
    g.get_top_k_important_stops()


def main():
    get_top_k_stop()


if __name__ == "__main__":
    main()
