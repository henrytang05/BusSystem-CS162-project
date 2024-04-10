import unittest
from src.models.RouteVar import RouteVar


class TestRouteVar(unittest.TestCase):
    def test_creation(self):
        route_var = RouteVar(
            RouteId=1,
            RouteVarId=101,
            RouteVarName="Sample Route",
            RouteVarShortName="SR",
            RouteNo="123",
            StartStop="Start",
            EndStop="End",
            Distance=10.5,
            Outbound=True,
            RunningTime=30.0,
        )

        self.assertEqual(route_var.RouteId, 1)
        self.assertEqual(route_var.RouteVarId, 101)
        self.assertEqual(route_var.RouteVarName, "Sample Route")
        self.assertEqual(route_var.RouteVarShortName, "SR")
        self.assertEqual(route_var.RouteNo, "123")
        self.assertEqual(route_var.StartStop, "Start")
        self.assertEqual(route_var.EndStop, "End")
        self.assertAlmostEqual(route_var.Distance, 10.5)
        self.assertTrue(route_var.Outbound)
        self.assertAlmostEqual(route_var.RunningTime, 30.0)

    def test_immutable(self):
        route_var = RouteVar(
            RouteId=1,
            RouteVarId=101,
            RouteVarName="Sample Route",
            RouteVarShortName="SR",
            RouteNo="123",
            StartStop="Start",
            EndStop="End",
            Distance=10.5,
            Outbound=True,
            RunningTime=30.0,
        )

        with self.assertRaises(AttributeError):
            route_var.RouteId = 2

        with self.assertRaises(AttributeError):
            route_var.RouteVarId = 102

        # Add assertions for other fields as well


if __name__ == "__main__":
    unittest.main()
