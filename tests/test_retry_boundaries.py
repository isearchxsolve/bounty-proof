import math
import random
import unittest
from unittest.mock import Mock

from src.retry import backoff_delays


class BackoffBoundaryTests(unittest.TestCase):
    def test_positive_jitter_is_capped_after_scaling(self):
        rng = Mock()
        rng.uniform.return_value = 0.5
        self.assertEqual(backoff_delays(3, base=20.0, cap=30.0, jitter=0.5, rng=rng),
                         [30.0, 30.0, 30.0])

    def test_negative_jitter_uses_uncapped_value(self):
        rng = Mock()
        rng.uniform.return_value = -0.5
        self.assertEqual(backoff_delays(3, base=20.0, cap=30.0, jitter=0.5, rng=rng),
                         [10.0, 20.0, 30.0])

    def test_zero_retries_does_not_consume_randomness(self):
        rng = Mock()
        self.assertEqual(backoff_delays(0, jitter=0.5, rng=rng), [])
        rng.uniform.assert_not_called()

    def test_long_policy_keeps_exact_count_and_hard_cap(self):
        for jitter in (0.0, 0.5):
            with self.subTest(jitter=jitter):
                delays = backoff_delays(1100, cap=60.0, jitter=jitter)
                self.assertEqual(len(delays), 1100)
                self.assertTrue(all(math.isfinite(d) and 0 <= d <= 60.0 for d in delays))
                self.assertEqual(delays[-1], 60.0)

    def test_overflowed_power_with_small_base_can_still_be_below_cap(self):
        delays = backoff_delays(1025, base=1e-300, cap=1e12)
        expected = math.ldexp(1e-300, 1024)
        self.assertTrue(math.isclose(delays[-1], expected, rel_tol=1e-12))
        self.assertLess(delays[-1], 1e12)

    def test_jitter_after_intermediate_product_overflow_can_restore_finite_value(self):
        rng = Mock()
        rng.uniform.return_value = -0.5
        delays = backoff_delays(2, base=1e308, factor=2.0, cap=1.5e308,
                                jitter=0.5, rng=rng)
        self.assertTrue(math.isclose(delays[1], 1e308, rel_tol=1e-12))

    def test_seeded_small_policies_match_the_documented_formula(self):
        for jitter in (0.0, 0.25, 0.75):
            rng = random.Random(42)
            oracle = random.Random(42)
            expected = [min(0.3 * 1.5 ** n *
                            (1 + oracle.uniform(-jitter, jitter) if jitter else 1), 30.0)
                        for n in range(30)]
            self.assertEqual(backoff_delays(30, base=0.3, factor=1.5, cap=30.0,
                                            jitter=jitter, rng=rng), expected)
            self.assertEqual(rng.getstate(), oracle.getstate())
