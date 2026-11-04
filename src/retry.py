"""Retry scheduling with exponential backoff and a hard cap."""
import math
import random


def backoff_delays(attempts, base=1.0, factor=2.0, cap=30.0, jitter=0.0, rng=None):
    """Return the delay in seconds to wait before each retry.

    ``attempts`` retries are scheduled, so the returned list holds exactly
    ``attempts`` entries. The delay for retry ``n`` (0-based) is
    ``base * factor ** n``, optionally scaled by a jitter factor drawn from
    ``[1 - jitter, 1 + jitter]``, then clamped to ``cap``.

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
    for n in range(attempts):
        multiplier = 1 + generator.uniform(-jitter, jitter) if jitter else 1
        try:
            delay = base * factor ** n * multiplier
        except OverflowError:
            delay = math.inf
        if math.isinf(delay):
            # The power can overflow even when a small base makes the final
            # delay representable. Only use logs on that exceptional path.
            log_delay = math.log(base) + n * math.log(factor) + math.log(multiplier)
            delay = cap if log_delay >= math.log(cap) else math.exp(log_delay)
        delays.append(min(delay, cap))
    return delays
