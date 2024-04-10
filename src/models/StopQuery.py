__all__ = ["StopQuery"]
import pandas as pd
import csv
from ..utils.constants import CWD, STOP_LIST, STOP_SEARCH_RESULTS
from .Stop import Stop
from ..utils.helpers import ensure_query_path_exists, ensure_valid_query
from ..utils import json_handler
from ..utils.Cache import Cache
from typing import Any


class StopQuery:
    """
    StopQuery class is used to query the Stop objects and output the result as csv or json

    Class Attributes:
    _cache: Cache
        a private attribute to store the cached data
        Cached data: Stop List, Stop Search Results, Route Stop Map

    Attributes:
    ----------
    query : tuple
        a tuple of (str, any) that represent the field and value
    result: list
        a list of Stop objects that meet the query

    Methods:
    --------
    search(field: str, value: any) -> list
        search for the query and return the result as a list of Stop objects

    output_as_csv(filename: str = "result.json") -> none
        output the query result to a csv file

    output_as_json(filename: str = "result.json") -> none
        output the query result to a json file

    Usage:
    ------
    ```python
    q = StopQuery()
    results = q.search(field = "StopId", value = 1)
    print(results)
    q.output_as_csv("result.csv")
    ```

    """

    _cache = Cache()

    def __new__(cls):
        """load the stop data upon the initilization of the first query"""
        if not Cache.get(STOP_LIST):
            Stop.load_stop()
        return super().__new__(cls)

    def __init__(self) -> None:
        self.result = []
        self.query = ()

    @property
    def query(self) -> tuple:
        return self._query

    @query.setter
    def query(self, item: tuple) -> None:
        self._query = item

    @property
    def result(self) -> list:
        return self._result

    @result.setter
    def result(self, value: list) -> None:
        self._result = value

    @ensure_valid_query(Stop)
    def search(self, field: str, value: Any) -> list:
        """
        Search for the stop objects that meet the query

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
            list of Stop objects

        """

        self.query = (field, value)
        if not Cache.get(STOP_SEARCH_RESULTS):
            Cache.add(STOP_SEARCH_RESULTS, {})

        if result := Cache.get(STOP_SEARCH_RESULTS).get(self.query):
            return result

        self.result = []
        for _, item in Cache.get(STOP_LIST).items():
            if getattr(item, field) == value:
                self.result.append(item)

        Cache.get(STOP_SEARCH_RESULTS)[(field, value)] = self.result
        return self.result

    @ensure_query_path_exists
    def output_as_csv(self, filename: str = "result.csv") -> None:
        """Query result is store in the {CWD}/query/ directory"""
        if not self.result:
            with open(f"{CWD}/query/{filename}", "w", encoding="utf-8") as file:
                file.write("Not Found Stop")
                return
        df = pd.DataFrame(list(item.__dict__ for item in self.result))
        df.to_csv(
            f"{CWD}/query/{filename}",
            index=False,
            quoting=csv.QUOTE_NONNUMERIC,
            encoding="utf-8",
        )

    @ensure_query_path_exists
    def output_as_json(self, filename: str = "result.json") -> None:
        """Query result is store in the {CWD}/query/ directory"""
        json_handler.writer(f"{CWD}/query/{filename}", self.result)
