__all__ = ["Edge"]


class Edge:
    def __init__(
        self,
        src: int,
        dest: int,
        time: float,
        routevar: tuple[int, int],
        path: tuple[int, int],
    ):
        self.src = src
        self.dest = dest
        self.time = time
        self.routevar = routevar
        self.path = path