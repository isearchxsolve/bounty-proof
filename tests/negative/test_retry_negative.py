import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.retry import backoff_delays  # noqa: E402


class BackoffDelaysNegativeTests(unittest.TestCase):
    """SCENARIO_NEGATIVE_FAILURE: malformed parameters are refused with ValueError."""

    def test_negative_attempts_is_refused(self):
        with self.assertRaises(ValueError):
            backoff_delays(-1)

    def test_non_integer_attempts_is_refused(self):
        for bad in ("3", 1.5, [3], {}, True):
            with self.subTest(value=bad):
                with self.assertRaises(ValueError):
                    backoff_delays(bad)

    def test_non_positive_base_is_refused(self):
        for bad in (0, -1.0):
            with self.subTest(base=bad):
                with self.assertRaises(ValueError):
                    backoff_delays(3, base=bad)

    def test_factor_below_one_is_refused(self):
        with self.assertRaises(ValueError):
            backoff_delays(3, factor=0.9)

    def test_non_positive_cap_is_refused(self):
        for bad in (0, -5.0):
            with self.subTest(cap=bad):
                with self.assertRaises(ValueError):
                    backoff_delays(3, cap=bad)

    def test_jitter_outside_its_band_is_refused(self):
        for bad in (1.0, 1.5, -0.1):
            with self.subTest(jitter=bad):
                with self.assertRaises(ValueError):
                    backoff_delays(3, jitter=bad)


if __name__ == "__main__":
    unittest.main()
