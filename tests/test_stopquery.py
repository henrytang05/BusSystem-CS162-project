import unittest
import os
from src.models.StopQuery import StopQuery
from src.models.Stop import Stop
from src.utils.Cache import Cache


class TestStopQuery(unittest.TestCase):
    def setUp(self):
        self.stop_query = StopQuery()
        self.stop = Stop(
            StopId=1,
            Code="Code1",
            Name="Stop1",
            StopType="Type1",
            Zone="Zone1",
            Ward="Ward1",
            AddressNo="AddressNo1",
            Street="Street1",
            SupportDisability="Yes",
            Status="Active",
            Lng=10.0,
            Lat=20.0,
            Search="Search1",
            Routes="Routes1",
        )
        Cache.add("Test Stop List", [self.stop])

    def test_search(self):
        result = self.stop_query.search(field="StopId", value=1)
        self.assertEqual(result[0].StopId, 1)

    def test_output_as_csv(self):
        self.stop_query.search(field="StopId", value=1)
        self.stop_query.output_as_csv("test_output.csv")
        self.assertTrue(os.path.exists(f"{os.getcwd()}/query/test_output.csv"))

    def test_output_as_json(self):
        self.stop_query.search(field="StopId", value=1)
        self.stop_query.output_as_json("test_output.json")
        self.assertTrue(os.path.exists(f"{os.getcwd()}/query/test_output.json"))

    def tearDown(self):
        Cache.remove("Test Stop List")
        if os.path.exists(f"{os.getcwd()}/query/test_output.csv"):
            os.remove(f"{os.getcwd()}/query/test_output.csv")
        if os.path.exists(f"{os.getcwd()}/query/test_output.json"):
            os.remove(f"{os.getcwd()}/query/test_output.json")


if __name__ == "__main__":
    unittest.main()
