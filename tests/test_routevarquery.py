import unittest
import os
from src.models.RouteVarQuery import RouteVarQuery
from src.models.RouteVar import Route, Var, VarData


class TestRouteVarQuery(unittest.TestCase):
    def setUp(self):
        self.route_var_query = RouteVarQuery()
        self.var = Var(
            VarData(
                RouteId=1,
                RouteVarId=1,
                RouteVarName="Sample RouteVar",
                RouteVarShortName="SRV",
                RouteNo="1",
                StartStop="Start",
                EndStop="End",
                Distance=10.0,
                Outbound=True,
                RunningTime=30.0,
            )
        )
        self.route = Route(self.var)

    def test_search(self):
        result = self.route_var_query.search(field="RouteId", value=1)
        self.assertEqual(result[0].RouteId, 1)

    def test_output_as_csv(self):
        self.route_var_query.search(field="RouteId", value=1)
        self.route_var_query.output_as_csv("test_output.csv")
        self.assertTrue(os.path.exists(f"{os.getcwd()}/query/test_output.csv"))

    def test_output_as_json(self):
        self.route_var_query.search(field="RouteId", value=1)
        self.route_var_query.output_as_json("test_output.json")
        self.assertTrue(os.path.exists(f"{os.getcwd()}/query/test_output.json"))

    #
    def tearDown(self):
        if os.path.exists(f"{os.getcwd()}/query/test_output.csv"):
            os.remove(f"{os.getcwd()}/query/test_output.csv")
        if os.path.exists(f"{os.getcwd()}/query/test_output.json"):
            os.remove(f"{os.getcwd()}/query/test_output.json")


if __name__ == "__main__":
    unittest.main()
