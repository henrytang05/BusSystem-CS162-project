import unittest
from src.utils.Cache import Cache


class TestCache(unittest.TestCase):
    def setUp(self):
        # Clear the cache before each test
        Cache.clear()

    def test_add_and_get(self):
        Cache.add("key1", "value1")
        self.assertEqual(Cache.get("key1"), "value1")

    def test_reset(self):
        Cache.add("key1", "value1")
        Cache.reset("key1", "new_value")
        self.assertEqual(Cache.get("key1"), "new_value")

    def test_get_keys(self):
        Cache.add("key1", "value1")
        Cache.add("key2", "value2")
        keys = Cache.get_keys()
        self.assertEqual(len(keys), 2)
        self.assertIn("key1", keys)
        self.assertIn("key2", keys)

    def test_remove(self):
        Cache.add("key1", "value1")
        Cache.remove("key1")
        self.assertIsNone(Cache.get("key1"))

    def test_clear(self):
        Cache.add("key1", "value1")
        Cache.add("key2", "value2")
        Cache.clear()
        self.assertEqual(len(Cache.get_keys()), 0)

    def test_singleton_instance(self):
        cache1 = Cache()
        cache2 = Cache()
        self.assertIs(cache1, cache2)

    def test_add_existing_key(self):
        Cache.add("key1", "value1")
        with self.assertRaises(ValueError):
            Cache.add("key1", "value2")


if __name__ == "__main__":
    unittest.main()
