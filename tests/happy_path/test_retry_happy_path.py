import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.retry import backoff_delays  # noqa: E402


class BackoffDelaysHappyPathTests(unittest.TestCase):
    """SCENARIO_HAPPY_PATH: valid retry budgets schedule the expected delays."""

    def test_returns_exactly_one_delay_per_retry(self):
        self.assertEqual(len(backoff_delays(3)), 3)

    def test_delays_grow_exponentially(self):
        self.assertEqual(backoff_delays(4, base=1.0, factor=2.0, cap=100.0),
                         [1.0, 2.0, 4.0, 8.0])

    def test_single_retry_schedules_the_base_delay(self):
        self.assertEqual(backoff_delays(1, base=0.5, factor=2.0, cap=30.0), [0.5])

    def test_delays_are_clamped_to_the_cap(self):
        self.assertEqual(backoff_delays(5, base=1.0, factor=10.0, cap=30.0),
                         [1.0, 10.0, 30.0, 30.0, 30.0])


if __name__ == "__main__":
    unittest.main()
