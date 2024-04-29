from networkx import MultiDiGraph


class Graph(MultiDiGraph):
    def __init__(self):
        super().__init__()


def main():
    g = Graph()
    g.add_node(3)
    g.add_nodes_from(range(100, 110))
    print(g.nodes)


if __name__ == "__main__":
    main()
