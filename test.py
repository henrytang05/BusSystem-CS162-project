def dis():
    loc1 = (1, 40)
    loc2 = (2, 50)
    distance = calculate_distance(loc1, loc2)
    print(distance)


def get_route():
    from src.models.RouteVarQuery import RouteVarQuery
    from src.models.StopQuery import StopQuery

    q = RouteVarQuery()
    q.search("RouteId", 1)

    # s = StopQuery()
    # s.search("StopId", 33)

    print(q.result)


def map_stop_to_path():
    from src.models.Path import PathHandler
    from src.models.Stop import StopHandler
    from src.models.RouteVar import RouteVarHandler

    rv = RouteVarHandler()
    rv.load()
    hd = StopHandler()
    hd.load()
    p = PathHandler()
    p.load()

    path = rv.get_var(3, 5).get_path()
    for seg in path:
        print(seg)


def main():

    map_stop_to_path()


if __name__ == "__main__":
    main()
