import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.retry import backoff_delays  # noqa: E402


class BackoffDelaysRegressionTests(unittest.TestCase):
    """SCENARIO_DEFECT_REGRESSION: issue #8 off-by-one and uncapped jitter."""

    def test_attempt_count_matches_the_documented_contract(self):
        # Regression: range(attempts + 1) returned one delay too many.
        for attempts in (0, 1, 2, 3, 7):
            with self.subTest(attempts=attempts):
                self.assertEqual(
                    len(backoff_delays(attempts)), attempts,
                    "backoff_delays(%d) must schedule exactly %d retries" % (attempts, attempts))

    def test_zero_attempts_returns_no_delays(self):
        # Regression: backoff_delays(0) used to return [1.0].
        self.assertEqual(backoff_delays(0), [],
                         "backoff_delays(0) must return no delays at all")

    def test_jittered_delays_never_exceed_the_hard_cap(self):
        # Regression: clamping before jitter let a delay exceed the hard ceiling.
        delays = backoff_delays(12, base=1.0, factor=10.0, cap=30.0, jitter=0.9)
        over = [delay for delay in delays if delay > 30.0]
        self.assertEqual(over, [],
                         "jittered delays must never exceed the configured cap")

    def test_unjittered_delays_grow_then_clamp(self):
        self.assertEqual(backoff_delays(5, base=1.0, factor=10.0, cap=30.0),
                         [1.0, 10.0, 30.0, 30.0, 30.0])


if __name__ == "__main__":
    unittest.main()
