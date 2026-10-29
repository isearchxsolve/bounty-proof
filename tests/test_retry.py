import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.retry import backoff_delays  # noqa: E402


class BackoffDelayTests(unittest.TestCase):
    def test_returns_one_delay_per_retry(self):
        self.assertEqual(len(backoff_delays(3)), 3)

    def test_zero_attempts_schedules_nothing(self):
        self.assertEqual(backoff_delays(0), [])

    def test_delays_grow_exponentially(self):
        self.assertEqual(backoff_delays(4, base=1.0, factor=2.0, cap=100.0),
                         [1.0, 2.0, 4.0, 8.0])

    def test_delays_are_clamped_to_the_cap(self):
        self.assertEqual(backoff_delays(5, base=1.0, factor=10.0, cap=30.0),
                         [1.0, 10.0, 30.0, 30.0, 30.0])

    def test_jitter_never_exceeds_the_cap(self):
        # The cap is a hard ceiling: jitter must not push a delay above it.
        for delay in backoff_delays(8, base=1.0, factor=10.0, cap=30.0, jitter=0.5):
            self.assertLessEqual(delay, 30.0)

    def test_jitter_stays_within_its_band(self):
        for delay in backoff_delays(6, base=1.0, factor=2.0, cap=100.0, jitter=0.25):
            self.assertGreaterEqual(delay, 0.0)

    def test_positive_jitter_is_clamped_after_scaling(self):
        class MaximumJitter:
            def uniform(self, lower, upper):
                return upper

        self.assertEqual(backoff_delays(1, base=8.0, cap=10.0, jitter=0.5,
                                        rng=MaximumJitter()), [10.0])

    def test_negative_jitter_scales_the_uncapped_delay(self):
        class MinimumJitter:
            def uniform(self, lower, upper):
                return lower

        self.assertEqual(backoff_delays(1, base=20.0, cap=10.0, jitter=0.5,
                                        rng=MinimumJitter()), [10.0])

    def test_zero_attempts_does_not_consume_randomness(self):
        class UnexpectedDraw:
            def uniform(self, lower, upper):
                raise AssertionError("no retry should consume randomness")

        self.assertEqual(backoff_delays(0, jitter=0.5, rng=UnexpectedDraw()), [])

    def test_negative_attempts_is_refused(self):
        with self.assertRaises(ValueError):
            backoff_delays(-1)

    def test_jitter_of_one_is_refused(self):
        with self.assertRaises(ValueError):
            backoff_delays(3, jitter=1.0)


if __name__ == "__main__":
    unittest.main()
