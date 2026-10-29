import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.duration import parse_duration  # noqa: E402


class ParseDurationTests(unittest.TestCase):
    def test_seconds_only(self):
        self.assertEqual(parse_duration("90s"), 90)

    def test_hours_and_minutes(self):
        self.assertEqual(parse_duration("1h30m"), 5400)

    def test_units_are_case_insensitive(self):
        self.assertEqual(parse_duration("1H30M"), 5400)
        self.assertEqual(parse_duration("2M"), 120)
        self.assertEqual(parse_duration("1H2m3S"), 3723)

    def test_zero_duration_is_valid(self):
        self.assertEqual(parse_duration("0s"), 0)
        self.assertEqual(parse_duration("0H0M0S"), 0)

    def test_invalid_input_raises(self):
        for text in ("abc", "", "   ", "123", "1d"):
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    parse_duration(text)


if __name__ == "__main__":
    unittest.main()
