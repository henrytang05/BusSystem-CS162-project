import unittest
from unittest.mock import MagicMock
from src.utils.helpers import ensure_valid_query, ensure_query_path_exists, intersection
import os


class TestUtils(unittest.TestCase):
    def test_ensure_valid_query_valid_field(self):
        class_name_mock = MagicMock()
        class_name_mock.__annotations__ = {"valid_field": int}

        @ensure_valid_query(class_name_mock)
        def test_function(field):
            return "Valid query"

        result = test_function(field="valid_field")
        self.assertEqual(result, "Valid query")

    def test_ensure_valid_query_invalid_field(self):
        class_name_mock = MagicMock()
        class_name_mock.__annotations__ = {"valid_field": int}

        @ensure_valid_query(class_name_mock)
        def test_function(field):
            return "Valid query"

        with self.assertRaises(ValueError):
            test_function(field="invalid_field")

    def test_ensure_query_path_exists_directory_exists(self):
        os.mkdir("test_query")
        test_function_mock = MagicMock()

        @ensure_query_path_exists
        def test_function():
            test_function_mock()
            return "Function executed"

        result = test_function()
        self.assertEqual(result, "Function executed")
        test_function_mock.assert_called_once()

        # Clean up
        os.rmdir("test_query")

    def test_ensure_query_path_exists_directory_does_not_exist(self):
        test_function_mock = MagicMock()

        @ensure_query_path_exists
        def test_function():
            test_function_mock()
            return "Function executed"

        result = test_function()
        self.assertEqual(result, "Function executed")
        test_function_mock.assert_called_once()

    def test_ensure_query_path_exists_existing_file(self):
        with open("query/test_file.txt", "w") as f:
            f.write("Test content")

        test_function_mock = MagicMock()

        @ensure_query_path_exists
        def test_function():
            test_function_mock()
            return "Function executed"

        result = test_function()
        self.assertEqual(result, "Function executed")
        test_function_mock.assert_called_once()

        # Clean up
        os.remove("query/test_file.txt")

    def test_intersection_multiple_lists(self):
        list1 = [1, 2, 3, 4, 5, 6]
        list2 = [1, 3, 4, 5, 6]
        list3 = [9, 32, 123, 4, 1, 1, 1]
        list4 = [1, 1, 1, 1, 4, 1, 1]

        result = intersection(list1, list2, list3, list4)
        self.assertEqual(result, list(set([1, 4])))

    def test_intersection_no_list(self):
        with self.assertRaises(ValueError):
            intersection()

    def test_intersection_one_list(self):
        list1 = [1, 2, 3, 4]
        result = intersection(list1)
        self.assertEqual(result, list(set([1, 2, 3, 4])))


if __name__ == "__main__":
    unittest.main()
