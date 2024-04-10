import unittest
from src.models.Stop import Stop


class TestStop(unittest.TestCase):
    def test_creation(self):
        stop = Stop(
            StopId=1,
            Code="ABC123",
            Name="Sample Stop",
            StopType="Bus Stop",
            Zone="A",
            Ward="Example Ward",
            AddressNo="123",
            Street="Example Street",
            SupportDisability="Yes",
            Status="Active",
            Lng=123.456,
            Lat=78.90,
            Search="Sample Search",
            Routes="Route 1, Route 2",
        )

        self.assertEqual(stop.StopId, 1)
        self.assertEqual(stop.Code, "ABC123")
        self.assertEqual(stop.Name, "Sample Stop")
        self.assertEqual(stop.StopType, "Bus Stop")
        self.assertEqual(stop.Zone, "A")
        self.assertEqual(stop.Ward, "Example Ward")
        self.assertEqual(stop.AddressNo, "123")
        self.assertEqual(stop.Street, "Example Street")
        self.assertEqual(stop.SupportDisability, "Yes")
        self.assertEqual(stop.Status, "Active")
        self.assertAlmostEqual(stop.Lng, 123.456)
        self.assertAlmostEqual(stop.Lat, 78.90)
        self.assertEqual(stop.Search, "Sample Search")
        self.assertEqual(stop.Routes, "Route 1, Route 2")


if __name__ == "__main__":
    unittest.main()
