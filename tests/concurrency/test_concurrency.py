import os
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.pagination import page_bounds  # noqa: E402


class PageBoundsConcurrencyTests(unittest.TestCase):
    """SCENARIO_CONCURRENCY_RACE: ``page_bounds`` is pure and race-free."""

    def test_concurrent_calls_return_consistent_bounds(self):
        pages = list(range(1, 51))

        def bounds(page):
            return page, page_bounds(page, 10)

        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(bounds, pages * 4))

        self.assertEqual(len(results), len(pages) * 4)
        for page, (start, end) in results:
            self.assertEqual((start, end), ((page - 1) * 10, page * 10))

    def test_concurrent_full_pages_never_drop_the_last_item(self):
        items = list(range(50))
        pages = [1, 2, 3, 4, 5] * 10

        def slice_for(page):
            start, end = page_bounds(page, 10)
            return items[start:end]

        with ThreadPoolExecutor(max_workers=8) as pool:
            chunks = list(pool.map(slice_for, pages))

        for page, chunk in zip(pages, chunks):
            self.assertEqual(chunk, list(range((page - 1) * 10, page * 10)))


if __name__ == "__main__":
    unittest.main()
