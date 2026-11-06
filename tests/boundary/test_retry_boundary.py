import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.retry import backoff_delays  # noqa: E402


class BackoffDelaysBoundaryTests(unittest.TestCase):
    """SCENARIO_NULL_INPUT / EMPTY_INPUT / BOUNDARY_LIMIT for ``backoff_delays``."""

    def test_none_attempts_is_refused(self):
        with self.assertRaises(ValueError):
            backoff_delays(None)

    def test_none_numeric_arguments_are_refused(self):
        for kwargs in ({"base": None}, {"factor": None}, {"cap": None}, {"jitter": None}):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError):
                    backoff_delays(3, **kwargs)

    def test_empty_attempt_budget_schedules_nothing(self):
        self.assertEqual(backoff_delays(0), [])

    def test_zero_attempts_with_jitter_schedules_nothing(self):
        self.assertEqual(backoff_delays(0, jitter=0.5), [])

    def test_zero_jitter_is_allowed(self):
        self.assertEqual(backoff_delays(2, jitter=0.0), [1.0, 2.0])

    def test_delay_equal_to_the_cap_is_kept_exactly(self):
        # base * factor ** 1 == cap is the exact ceiling boundary.
        self.assertEqual(backoff_delays(2, base=15.0, factor=2.0, cap=30.0), [15.0, 30.0])

    def test_first_retry_uses_the_base_delay(self):
        self.assertEqual(backoff_delays(1, base=2.0, factor=3.0, cap=100.0), [2.0])


if __name__ == "__main__":
    unittest.main()
