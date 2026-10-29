To address the issues in the `backoff_delays` function, the loop is adjusted to run the correct number of times, and the order of applying jitter and the cap is corrected.

Here is the fixed code:

```python
def backoff_delays(attempts, base=2.0, max_jitter=1.0, cap=60.0):
    delays = []
    for n in range(attempts):
        delay = base * (2 ** n)
        delay = delay * (1 + max_jitter * random.random())
        delay = min(delay, cap)
        delays.append(float(delay))
    return delays
```