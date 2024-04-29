__all__ = [
    "ensure_valid_query",
    "ensure_query_path_exists",
    "intersection",
    "calculate_distance",
    "visualize",
]
import os
from pyproj import Geod
from .constants import PATH_LIST, STOP_LIST
from .Cache import Cache


CWD = os.getcwd()


def visualize(features_collection: list, file_path: str = "path.geojson") -> None:
    from geojson import FeatureCollection
    import os

    cwd = os.getcwd()
    with open(f"{cwd}/output/{file_path}", "w") as file:
        file.write(str(FeatureCollection(features_collection)))


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
