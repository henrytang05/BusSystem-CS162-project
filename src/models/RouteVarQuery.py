__all__ = ["RouteVarQuery"]
# import pandas as pd
from ..utils.constants import CWD, VAR_LIST, VAR_SEARCH_RESULT
import csv
from .RouteVar import RouteVar
from ..utils.helpers import ensure_query_path_exists, ensure_valid_query
from ..utils import json_handler
from ..utils.Cache import Cache
from typing import Any


class RouteVarQuery:
    """
    RouteVarQuery class is used to query the RouteVar objects and output the result as csv or json

    Class Attributes:
    -----------
    _cache: Cache
        a private attribute to store the cached data
        Cached data: Route Var List, Route Var Search Results


    Attributes:
    ----------
    query : tuple
        a tuple of (str, any) that represent the field and value
    result: list
        a list of RouteVar objects that meet the query

    Methods:
    --------
    search(field: str, value: any) -> list
        search for the query and return the result as a list of RouteVar objects

    output_as_csv(filename: str = "result.json") -> none
        output the query result to a csv file

    output_as_json(filename: str = "result.json") -> none
        output the query result to a json file

    Usage:
    -------
    ```python
    q = RouteVarQuery()
    results = q.search(field = "RouteId", value = 1)
    print(results)
    q.output_as_json("result.json")
    ```

    """

    _cache = Cache()

    def __new__(cls):
        """load the route var data upon the initilization of the first query"""
        if not Cache.get(VAR_LIST):
            RouteVar.load_route_var()
        return super().__new__(cls)

    def __init__(self):
        self.result = []
        self.query = ()

    @property
    def query(self) -> tuple:
        return self._query

    @query.setter
    def query(self, item: tuple):
        self._query = item

    @property
    def result(self) -> list[RouteVar]:
        return self._result

    @result.setter
    def result(self, value: list):
        self._result = value

    @ensure_valid_query(RouteVar)
    def search(self, field: str, value: Any) -> list:
        """
        Search for the route var objects that meet the query

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
            list of RouteVar objects


        """

        self.query = (field, value)
        if not Cache.get(VAR_SEARCH_RESULT):
            Cache.add(VAR_SEARCH_RESULT, {})

        if result := Cache.get(VAR_SEARCH_RESULT).get(self.query):
            self.result = result
            return result

        self.result = []
        for _, item in Cache.get(VAR_LIST).items():
            if getattr(item, field) == value:
                self.result.append(item)

        Cache.get(VAR_SEARCH_RESULT)[(field, value)] = self.result
        return self.result

    @ensure_query_path_exists
    def output_as_csv(self, filename: str = "result.csv"):
        """Query result is store in the {CWD}/query/ directory"""
        if not self.result:
            with open(f"{CWD}/query/{filename}", "w", encoding="utf-8") as file:
                file.write("Not Found Route")
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
