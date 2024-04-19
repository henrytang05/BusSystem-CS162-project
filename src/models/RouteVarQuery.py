__all__ = ["RouteVarQuery"]
import pandas as pd
from ..utils.constants import CWD
import csv
import functools
from .RouteVar import RouteVarHandler, Var, Route
from ..utils.helpers import ensure_query_path_exists
from ..utils import json_handler
from typing import Any
from .Query import Query


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

    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def route_var_list(self) -> dict[int, Route]:
        if not self._route_var_list:
            self._route_var_list: dict[int, Route] = RouteVarHandler().get_route_list()
        return self._route_var_list

    @property
    def result(self) -> list[Var]:
        return self._result

    @result.setter
    def result(self, value: list[Var]) -> None:
        self._result = value

    @property
    def query(self) -> Query:
        return self._query

    @query.setter
    def query(self, value: Query) -> None:
        self._query = value

    @functools.lru_cache(maxsize=None)
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

        self.query = Query(field, value)

        if not self.query.is_valid("VarData", field):
            raise ValueError(f"{field} is not a valid field")

        if field == "RouteId":
            self.result = list(self.route_var_list[value].get_vars().values())
        else:
            for route in self.route_var_list.values():
                for var in route.vars.values():
                    if getattr(var.data, field) == value:
                        self.result.append(var)

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
