__all__ = ["PathQuery"]
import pandas as pd
import csv
import functools
from .Path import Path, PathData
from ..utils.constants import CWD, PATH_LIST, PATH_SEARCH_RESULTS
from ..utils.helpers import ensure_query_path_exists, ensure_valid_query
from ..utils import json_handler
from typing import Any
from .Query import Query


class PathQuery:
    """
    PathQuery class is used to query the Path objects and output the result as csv or json

    Class Attributes:
    -----------
    _cache: Cache
        a private attribute to store the cached data
        Cached data: Path List, Path Search Results


    Attributes:
    ----------
    query : tuple
        a tuple of (str, any) that represent the field and value
    result: list
        a list of Path objects that meet the query

    Methods:
    --------
    search(field: str, value: any) -> list
        search for the query and return the result as a list of Path objects

    output_as_csv(filename: str = "result.json") -> none
        output the query result to a csv file

    output_as_json(filename: str = "result.json") -> none
        output the query result to a json file

    Usage:
    -------
    ```python
    q = PathQuery()
    results = q.search(field = "RouteId", value = 1)
    print(results)
    q.output_as_json("result.json")
    ```

    """

    def __init__(self):
        from .Path import PathHandler

        self.handler = PathHandler()

    @property
    def path_list(self) -> dict[tuple[int, int], Path]:
        return self.handler.get_path_list()

    @property
    def result(self) -> list[PathData]:
        return self._result

    @result.setter
    def result(self, value: list[PathData]) -> None:
        self._result = value

    @property
    def query(self) -> Query:
        return self._query

    @query.setter
    def query(self, value: Query) -> None:
        if not value.is_valid(PathData):
            raise ValueError(f"{value.value} is not a valid field")
        self._query = value

    @functools.lru_cache(maxsize=None)
    def search(self, field: str, value: Any) -> list:
        """
        Search for the path objects that meet the query

        Parameters:
        ----------
        field : str
            The field you want to query

        value: any
            The value you want to query

        Raises:
        ------
        ValueError
            if field is not a str or doesn't exist

        Return:
        -------
            list of Path objects

        """

        self.query = (field, value)
        if not Cache.get(PATH_SEARCH_RESULTS):
            Cache.add(PATH_SEARCH_RESULTS, {})

        if result := Cache.get(PATH_SEARCH_RESULTS).get(self.query):
            self.result = result
            return result

        precision = 10e-3
        self.result = []

        for _, item in Cache.get(PATH_LIST).items():
            if field in ["lats", "lngs"]:
                locs = getattr(item, field)
                for loc in locs:
                    if abs(loc - value) <= precision:
                        self.result.append(item)
            elif field == "lng_lat_list":
                for pair in item.lng_lat_list:
                    if (
                        abs(pair[0] - value[0]) <= precision
                        and abs(pair[1] - value[1]) <= precision
                    ):
                        self.result.append(item)

            else:
                if getattr(item, field) == value:
                    self.result.append(item)
        Cache.get(PATH_SEARCH_RESULTS)[(field, value)] = self.result
        return self.result

    @ensure_query_path_exists
    def output_as_csv(self, filename: str = "result.csv"):
        """Query result is store in the {CWD}/query/ directory"""
        if not self.result:
            with open(f"{CWD}/query/{filename}", "w", encoding="utf-8") as file:
                file.write("Not Found")
                return
        df = pd.DataFrame(list(item.__dict__ for item in self.result))
        df.to_csv(
            f"{CWD}/query/{filename}",
            index=False,
            quoting=csv.QUOTE_NONNUMERIC,
            encoding="utf-8",
        )

    @ensure_query_path_exists
    def output_as_json(self, filename: str = "result.json"):
        """Query result is store in the {CWD}/query/ directory"""
        json_handler.writer(f"{CWD}/query/{filename}", self.result)
