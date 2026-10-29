import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.pagination import page_bounds  # noqa: E402


class PageBoundsNegativeTests(unittest.TestCase):
    """SCENARIO_NEGATIVE_FAILURE: malformed input is refused with ValueError."""

    def test_negative_page_is_refused(self):
        with self.assertRaises(ValueError):
            page_bounds(-1, 10)

    def test_negative_per_page_is_refused(self):
        with self.assertRaises(ValueError):
            page_bounds(1, -10)

    def test_float_page_is_refused(self):
        with self.assertRaises(ValueError):
            page_bounds(1.5, 10)

    def test_float_per_page_is_refused(self):
        with self.assertRaises(ValueError):
            page_bounds(1, 10.5)

    def test_non_integer_page_is_refused(self):
        with self.assertRaises(ValueError):
            page_bounds("1", 10)

    def test_malformed_payloads_never_silently_succeed(self):
        for bad in (None, "1", [1], {}, 0, -1):
            with self.subTest(value=bad):
                with self.assertRaises(ValueError):
                    page_bounds(bad, 10)


if __name__ == "__main__":
    unittest.main()
