"""Retry scheduling with exponential backoff and a hard cap."""
import random


def backoff_delays(attempts, base=1.0, factor=2.0, cap=30.0, jitter=0.0, rng=None):
    """Return the delay in seconds to wait before each retry.

    ``attempts`` retries are scheduled, so the returned list holds exactly
    ``attempts`` entries. The delay for retry ``n`` (0-based) is
    ``base * factor ** n``, clamped to ``cap``, then optionally scaled by a
    jitter factor drawn from ``[1 - jitter, 1 + jitter]``.

    The cap is a hard ceiling: no returned delay may exceed it, with or without
    jitter. ``jitter`` must be in ``[0, 1)``.
    """
    if attempts < 0:
        raise ValueError("attempts must be 0 or greater")
    if base <= 0:
        raise ValueError("base must be positive")
    if factor < 1:
        raise ValueError("factor must be 1 or greater")
    if cap <= 0:
        raise ValueError("cap must be positive")
    if not 0 <= jitter < 1:
        raise ValueError("jitter must be in [0, 1)")
    generator = rng or random.Random(0)
    delays = []
    for n in range(attempts + 1):
        delay = min(base * factor ** n, cap)
        if jitter:
            delay = delay * (1 + generator.uniform(-jitter, jitter))
        delays.append(delay)
    return delays
