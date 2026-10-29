import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.pagination import page_bounds  # noqa: E402


class PageBoundsRegressionTests(unittest.TestCase):
    """SCENARIO_DEFECT_REGRESSION: issue #3 dropped the last item of a full page."""

    def test_full_pages_do_not_drop_the_last_item(self):
        items = list(range(25))
        for page in (1, 2):
            with self.subTest(page=page):
                start, end = page_bounds(page, 10)
                self.assertEqual(
                    items[start:end], list(range((page - 1) * 10, page * 10)),
                    "full page must not drop its last item")

    def test_end_is_the_exclusive_bound(self):
        self.assertEqual(page_bounds(1, 10), (0, 10))
        self.assertEqual(page_bounds(2, 10), (10, 20))
        self.assertEqual(page_bounds(3, 10), (20, 30))

    def test_every_full_page_yields_per_page_items(self):
        items = list(range(100))
        for page in range(1, 11):
            with self.subTest(page=page):
                start, end = page_bounds(page, 10)
                self.assertEqual(len(items[start:end]), 10)


if __name__ == "__main__":
    unittest.main()
