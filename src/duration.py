"""Parse compact duration strings such as ``1h30m`` into seconds."""
import re

_UNITS = {"h": 3600, "m": 60, "s": 1}
_GROUPS = re.compile(r"(\d+)([hms])", re.IGNORECASE)


def parse_duration(text):
    """Return the number of seconds described by a compact duration string.

    Supported form: one or more ``<integer><unit>`` groups, for example ``"1h30m"``,
    ``"90s"`` or ``"2m30s"``. Units are ``h`` (hours), ``m`` (minutes) and ``s``
    (seconds), matched case-insensitively. Raise ValueError when no supported
    group is present.
    """
    groups = _GROUPS.findall(text)
    if not groups:
        raise ValueError("Duration must contain at least one integer and unit")
    total = 0
    for value, unit in groups:
        total += int(value) * _UNITS[unit.lower()]
    return total
