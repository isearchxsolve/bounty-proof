"""Parse compact duration strings such as ``1h30m`` into seconds."""
import re

_UNITS = {"h": 3600, "m": 60, "s": 1}
_GROUPS = re.compile(r"(\d+)([hms])", re.IGNORECASE)


def parse_duration(text):
    """Return the number of seconds described by a compact duration string.

    Supported form: one or more ``<integer><unit>`` groups, for example ``"1h30m"``,
    ``"90s"`` or ``"2m30s"``. Units are ``h`` (hours), ``m`` (minutes) and ``s``
    (seconds), and are accepted case-insensitively. Any other input, including an
    empty or malformed string, raises ``ValueError``.
    """
    if not isinstance(text, str):
        raise ValueError("duration must be a string")
    total = 0
    position = 0
    for match in _GROUPS.finditer(text):
        if match.start() != position:
            raise ValueError("invalid duration: " + repr(text))
        value, unit = match.group(1), match.group(2).lower()
        total += int(value) * _UNITS[unit]
        position = match.end()
    if not text or position != len(text):
        raise ValueError("invalid duration: " + repr(text))
    return total
