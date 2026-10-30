import os
import random
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.retry import backoff_delays  # noqa: E402


class BackoffDelaysConcurrencyTests(unittest.TestCase):
    """SCENARIO_CONCURRENCY_RACE: ``backoff_delays`` is pure and race-free."""

    def test_concurrent_calls_return_consistent_schedules(self):
        attempts = list(range(0, 25))

        def schedule(n):
            return n, backoff_delays(n, base=1.0, factor=2.0, cap=30.0)

        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(schedule, attempts * 4))

        self.assertEqual(len(results), len(attempts) * 4)
        for n, delays in results:
            self.assertEqual(len(delays), n)
            self.assertTrue(all(delay <= 30.0 for delay in delays))

    def test_concurrent_seeded_jitter_calls_are_deterministic(self):
        def schedule(_):
            return backoff_delays(5, base=1.0, factor=3.0, cap=30.0, jitter=0.5,
                                  rng=random.Random(0))

        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(schedule, range(40)))

        first = results[0]
        for delays in results[1:]:
            self.assertEqual(delays, first)


if __name__ == "__main__":
    unittest.main()
