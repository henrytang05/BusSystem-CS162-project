import unittest
import os
from src.models.PathQuery import PathQuery
from src.models.Path import Path
from src.utils.Cache import Cache


class TestPathQuery(unittest.TestCase):
    def setUp(self):
        self.path_query = PathQuery()

        lng_lat_list = [(10.0, 20.0), (30.0, 40.0)]
        lats = [20.0, 40.0]
        lngs = [10.0, 30.0]
        RouteId = 1
        RouteVarId = 1

        self.path = Path(
            lng_lat_list=lng_lat_list,
            lats=lats,
            lngs=lngs,
            RouteId=RouteId,
            RouteVarId=RouteVarId,
        )

        Cache.add("Test Path List", [self.path])

    def test_search(self):
        result = self.path_query.search(field="RouteId", value=1)
        self.assertEqual(result[0].RouteId, 1)

    def test_output_as_csv(self):
        self.path_query.search(field="RouteId", value=1)
        self.path_query.output_as_csv("test_output.csv")
        self.assertTrue(os.path.exists(f"{os.getcwd()}/query/test_output.csv"))

    def test_output_as_json(self):
        self.path_query.search(field="RouteId", value=1)
        self.path_query.output_as_json("test_output.json")
        self.assertTrue(os.path.exists(f"{os.getcwd()}/query/test_output.json"))

    def tearDown(self):
        Cache.remove("Test Path List")
        if os.path.exists(f"{os.getcwd()}/query/test_output.csv"):
            os.remove(f"{os.getcwd()}/query/test_output.csv")
        if os.path.exists(f"{os.getcwd()}/query/test_output.json"):
            os.remove(f"{os.getcwd()}/query/test_output.json")


if __name__ == "__main__":
    unittest.main()
