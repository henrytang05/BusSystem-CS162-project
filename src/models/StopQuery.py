__all__ = ["StopQuery"]
import pandas as pd
from ..utils.constants import CWD
import csv
import functools
from .Stop import StopHandler, StopData, Stop
from ..utils.helpers import ensure_path_exists
from ..utils import json_handler
from typing import Any
from .Query import Query


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

    def __init__(self):
        self.handler = StopHandler()
        self.result = []

    @property
    def stop_list(self) -> dict[int, Stop]:
        return self.handler.get_stops()

    @property
    def result(self) -> list[StopData]:
        return self._result

    @result.setter
    def result(self, value: list[StopData]) -> None:
        self._result = value

    @property
    def query(self) -> Query:
        return self._query

    @query.setter
    def query(self, value: Query) -> None:
        if not value.is_valid(StopData):
            raise ValueError(f"{value.value} is not a valid field")
        self._query = value

    # @functools.lru_cache(maxsize=None)
    def search(self, field: str, value) -> list[StopData]:

        self.query = Query(field, value)

        if field == "StopId":
            if self.query.value not in self.stop_list.keys():
                self.result = []
            else:
                self.result = [self.stop_list[self.query.value].data]
        else:
            for stop in self.stop_list:
                cv = getattr(self.stop_list[stop].data, self.query.field)
                if isinstance(cv, str):
                    assert isinstance(self.query.value, str)
                    if cv.lower() == self.query.value.lower():
                        self.result.append(self.stop_list[stop].data)
                else:
                    if cv == self.query.value:
                        self.result.append(self.stop_list[stop].data)
        return self.result

    @ensure_path_exists("query")
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

    @ensure_path_exists("query")
    def output_as_json(self, filename: str = "result.json") -> None:
        """Query result is store in the {CWD}/query/ directory"""
        json_handler.writer(f"{CWD}/query/{filename}", self.result)
