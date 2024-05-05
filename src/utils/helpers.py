__all__ = [
    "timeit",
    "ensure_valid_query",
    "ensure_path_exists",
    "intersection",
    "calculate_distance",
]
import os
from pyproj import Geod
from .constants import PATH_LIST, STOP_LIST
from .Cache import Cache


CWD = os.getcwd()


def timeit(func):
    import time

    count = 0
    cache = {}

    def wrapper(*args, **kwargs):
        nonlocal count
        nonlocal cache
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        count += 1
        cache[func.__name__] = (
            1 if cache.get(func.__name__) is None else cache[func.__name__] + 1
        )
        print(
            func.__name__, cache[func.__name__], ":Total time:", end - start, "seconds"
        )
        return result

    return wrapper


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


def ensure_path_exists(path: str):
    def wrapped(func):
        """Ensure the path for query exists before writing the file"""

        def make_directory(*args, **kwargs):
            nonlocal path
            path = kwargs.get("path", os.getcwd())
            try:
                os.makedirs(os.path.join(os.getcwd(), path), exist_ok=True)
            except OSError as e:
                print(f"Error creating directory: {e}")
            return func(*args, **kwargs)

        return make_directory

    return wrapped
