import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.pagination import page_bounds  # noqa: E402


class PageBoundsHappyPathTests(unittest.TestCase):
    """SCENARIO_HAPPY_PATH: valid pages return complete half-open slices."""

    def test_first_page_holds_a_full_page(self):
        items = list(range(25))
        start, end = page_bounds(1, 10)
        self.assertEqual(items[start:end], list(range(10)))

    def test_second_page_holds_a_full_page(self):
        items = list(range(25))
        start, end = page_bounds(2, 10)
        self.assertEqual(items[start:end], list(range(10, 20)))

    def test_partial_last_page_holds_the_remainder(self):
        items = list(range(25))
        start, end = page_bounds(3, 10)
        self.assertEqual(items[start:end], list(range(20, 25)))

    def test_bounds_are_plain_ints(self):
        self.assertEqual(page_bounds(1, 10), (0, 10))
        self.assertEqual(page_bounds(4, 25), (75, 100))


if __name__ == "__main__":
    unittest.main()
