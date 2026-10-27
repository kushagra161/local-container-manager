"""
test_utils.py
Unit Tests for utility functions
Student: Kushagra Kaushik | Roll: S24BCAU0112
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.utils import (
    validate_port_mapping,
    validate_container_name,
    format_size,
    truncate,
    parse_env_list,
)


class TestValidatePortMapping(unittest.TestCase):

    def test_valid_simple_port(self):
        self.assertTrue(validate_port_mapping("8080:80"))

    def test_valid_with_ip(self):
        self.assertTrue(validate_port_mapping("0.0.0.0:8080:80"))

    def test_invalid_missing_colon(self):
        self.assertFalse(validate_port_mapping("8080"))

    def test_invalid_empty(self):
        self.assertFalse(validate_port_mapping(""))

    def test_invalid_text(self):
        self.assertFalse(validate_port_mapping("abc:xyz"))


class TestValidateContainerName(unittest.TestCase):

    def test_valid_simple_name(self):
        self.assertTrue(validate_container_name("mycontainer"))

    def test_valid_name_with_dash(self):
        self.assertTrue(validate_container_name("my-container"))

    def test_valid_name_with_underscore(self):
        self.assertTrue(validate_container_name("my_container"))

    def test_invalid_starts_with_dash(self):
        self.assertFalse(validate_container_name("-bad"))

    def test_invalid_empty(self):
        self.assertFalse(validate_container_name(""))

    def test_invalid_special_chars(self):
        self.assertFalse(validate_container_name("my container!"))


class TestFormatSize(unittest.TestCase):

    def test_bytes(self):
        self.assertIn("B", format_size(512))

    def test_kilobytes(self):
        self.assertIn("KB", format_size(2048))

    def test_megabytes(self):
        self.assertIn("MB", format_size(5 * 1024 * 1024))

    def test_gigabytes(self):
        self.assertIn("GB", format_size(2 * 1024 ** 3))


class TestTruncate(unittest.TestCase):

    def test_short_string_unchanged(self):
        self.assertEqual(truncate("hello", 40), "hello")

    def test_long_string_truncated(self):
        result = truncate("a" * 50, 40)
        self.assertEqual(len(result), 40)
        self.assertTrue(result.endswith("..."))

    def test_exact_length_unchanged(self):
        s = "a" * 40
        self.assertEqual(truncate(s, 40), s)


class TestParseEnvList(unittest.TestCase):

    def test_single_var(self):
        result = parse_env_list(["FOO=bar"])
        self.assertEqual(result, {"FOO": "bar"})

    def test_multiple_vars(self):
        result = parse_env_list(["A=1", "B=2"])
        self.assertEqual(result["A"], "1")
        self.assertEqual(result["B"], "2")

    def test_value_with_equals(self):
        result = parse_env_list(["DB_URL=postgres://localhost:5432/db"])
        self.assertEqual(result["DB_URL"], "postgres://localhost:5432/db")

    def test_none_input(self):
        result = parse_env_list(None)
        self.assertEqual(result, {})

    def test_invalid_entry_skipped(self):
        result = parse_env_list(["INVALID", "GOOD=yes"])
        self.assertNotIn("INVALID", result)
        self.assertEqual(result["GOOD"], "yes")


if __name__ == "__main__":
    unittest.main(verbosity=2)
