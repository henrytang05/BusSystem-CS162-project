__all__ = [
    "ensure_valid_query",
    "ensure_query_path_exists",
    "intersection",
    "calculate_distance",
    "distance_finder",
    "stop_finder",
]
import os
from pyproj import Geod
from .constants import PATH_LIST, STOP_LIST
from .Cache import Cache


CWD = os.getcwd()


def stop_finder(routevar):
    last_found = 0
    if not Cache.get(PATH_LIST).get(routevar):
        raise ValueError("You haven't loaded path yet")

    path = Cache.get(PATH_LIST)[routevar]

    def find(stop: tuple[float, float]) -> int:
        """Return the index of the point on the Path corresponding to the stop"""
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


def distance_finder(routevar):
    pf = stop_finder(routevar)

    def find_distance(stop1, stop2) -> tuple[float, tuple[int, int]]:
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
        return (geo.line_length(lngs, lats), (index1, index2))

    return find_distance


def calculate_distance(loc1: tuple[float, float], loc2: tuple[float, float]) -> float:
    """
    Calculate the distance between two points

    Parameters:
    ----------
    loc1 : tuple[float, float]
        the geographical coordinates of the first point (lng, lat)

    loc2 : tuple[float, float]
        the geographical coordinates of the first point (lng, lat)

    Return:
    -------
        distance between 2 points

    Usage:
    ```python
    loc1 = (106, 10)
    loc2 = (0, 0)
    distance = calculate_distance(loc1, loc2)
    ```

    """

    lng_lat = list(zip(loc1, loc2))
    geo = Geod(ellps="WGS84")
    return geo.line_length(lng_lat[0], lng_lat[1])


def intersection(*args: list) -> list:
    """Intersection of multiple sets"""
    if len(args) <= 0:
        raise ValueError("Intersection requires at least 1 argument")

    sets = [set(lst) for lst in args]

    return list(set.intersection(*sets))


def ensure_valid_query(class_name):
    def decorator_function(func):
        def validate_query(*args, **kwargs):
            if kwargs["field"] in class_name.__annotations__.keys():
                return func(*args, **kwargs)
            else:
                raise ValueError(
                    "Invalid query",
                    "Available fields:",
                    class_name.__annotations__.keys(),
                )

        return validate_query

    return decorator_function


def ensure_query_path_exists(func):
    """Ensure the path for query exists before writing the file"""

    def make_directory(*argc, **kwargs):
        if not os.path.exists(f"{CWD}/query"):
            os.mkdir(f"{CWD}/query")
        return func(*argc, **kwargs)

    return make_directory
