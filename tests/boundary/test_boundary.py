import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.pagination import page_bounds  # noqa: E402


class PageBoundsBoundaryTests(unittest.TestCase):
    """SCENARIO_NULL_INPUT / EMPTY_INPUT / BOUNDARY_LIMIT for ``page_bounds``."""

    def test_none_page_is_refused(self):
        with self.assertRaises(ValueError):
            page_bounds(None, 10)

    def test_none_per_page_is_refused(self):
        with self.assertRaises(ValueError):
            page_bounds(1, None)

    def test_empty_string_input_is_refused(self):
        with self.assertRaises(ValueError):
            page_bounds("", 10)

    def test_empty_collection_input_is_refused(self):
        with self.assertRaises(ValueError):
            page_bounds([], 10)

    def test_page_zero_is_refused(self):
        with self.assertRaises(ValueError):
            page_bounds(0, 10)

    def test_per_page_zero_is_refused(self):
        with self.assertRaises(ValueError):
            page_bounds(1, 0)

    def test_smallest_valid_page_is_one(self):
        self.assertEqual(page_bounds(1, 1), (0, 1))

    def test_start_is_inclusive_and_end_is_exclusive(self):
        start, end = page_bounds(3, 4)
        self.assertEqual((start, end), (8, 12))
        items = list(range(20))
        self.assertEqual(items[start:end], [8, 9, 10, 11])

    def test_empty_collection_yields_empty_page(self):
        items = []
        start, end = page_bounds(1, 10)
        self.assertEqual(items[start:end], [])

    def test_large_page_number_stays_consistent(self):
        per_page = 10
        page = 10 ** 6
        self.assertEqual(page_bounds(page, per_page), ((page - 1) * per_page, page * per_page))


if __name__ == "__main__":
    unittest.main()
