__all__ = ["PathQuery"]
import pandas as pd
import csv
from .Path import Path, PathData
from ..utils.constants import CWD, PATH_LIST, PATH_SEARCH_RESULTS
from ..utils.helpers import ensure_path_exists
from ..utils import json_handler
from typing import Any
from .Query import Query


class PathQuery:
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

    # @property
    # def query(self) -> Query:
    #     return self._query
    #
    # @query.setter
    # def query(self, value: Query) -> None:
    #     if not value.is_valid(PathData):
    #         raise ValueError(f"{value.value} is not a valid field")
    #     self._query = value

    def search(self, routeid, varid) -> list:
        self.result.append(self.path_list[(routeid, varid)].data)

        return self.result

    @ensure_path_exists("query")
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

    def output_as_json(self, filename: str = "result.json"):
        """Query result is store in the {CWD}/query/ directory"""
        json_handler.writer(f"{CWD}/query/{filename}", self.result)
