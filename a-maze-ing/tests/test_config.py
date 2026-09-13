"""Unit tests for the MazeConfig parser and validation logic."""

import os
import tempfile
import unittest

from mazegen.config import ConfigError, parse_config_file


class TestConfigParser(unittest.TestCase):
    """Test suite for configuration parsing and validation."""

    def _create_temp_config(self, content: str) -> str:
        """Create a temporary config file with given content."""
        fd, path = tempfile.mkstemp(suffix=".txt")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_valid_default_config(self) -> None:
        """Test parsing the default valid configuration."""
        content = (
            "# This is a comment\n"
            "WIDTH=20\n"
            "HEIGHT=15\n"
            "ENTRY=0,0\n"
            "EXIT=19,14\n"
            "OUTPUT_FILE=maze.txt\n"
            "PERFECT=True\n"
        )
        filepath = self._create_temp_config(content)
        try:
            config = parse_config_file(filepath)
            self.assertEqual(config.width, 20)
            self.assertEqual(config.height, 15)
            self.assertEqual(config.entry, (0, 0))
            self.assertEqual(config.exit, (19, 14))
            self.assertEqual(config.output_file, "maze.txt")
            self.assertTrue(config.perfect)
            self.assertIsNone(config.seed)
        finally:
            os.remove(filepath)

    def test_optional_seed_parsing(self) -> None:
        """Test parsing configuration with optional SEED."""
        content = (
            "WIDTH=10\n"
            "HEIGHT=10\n"
            "ENTRY=0,0\n"
            "EXIT=9,9\n"
            "OUTPUT_FILE=maze.txt\n"
            "PERFECT=False\n"
            "SEED=4242\n"
        )
        filepath = self._create_temp_config(content)
        try:
            config = parse_config_file(filepath)
            self.assertFalse(config.perfect)
            self.assertEqual(config.seed, 4242)
        finally:
            os.remove(filepath)

    def test_missing_mandatory_key(self) -> None:
        """Test that missing mandatory keys raise ConfigError."""
        content = (
            "WIDTH=10\n"
            "HEIGHT=10\n"
            "ENTRY=0,0\n"
            "EXIT=9,9\n"
            "OUTPUT_FILE=maze.txt\n"
        )
        filepath = self._create_temp_config(content)
        try:
            with self.assertRaises(ConfigError) as ctx:
                parse_config_file(filepath)
            self.assertIn("Missing mandatory", str(ctx.exception))
        finally:
            os.remove(filepath)

    def test_syntax_error_missing_equals(self) -> None:
        """Test that lines without '=' raise ConfigError."""
        content = "WIDTH 10\n"
        filepath = self._create_temp_config(content)
        try:
            with self.assertRaises(ConfigError) as ctx:
                parse_config_file(filepath)
            self.assertIn("Syntax error", str(ctx.exception))
        finally:
            os.remove(filepath)

    def test_coordinates_out_of_bounds(self) -> None:
        """Test that coordinates out of maze bounds raise ConfigError."""
        content = (
            "WIDTH=10\n"
            "HEIGHT=10\n"
            "ENTRY=0,0\n"
            "EXIT=10,5\n"  # 10 is >= width (10)
            "OUTPUT_FILE=maze.txt\n"
            "PERFECT=True\n"
        )
        filepath = self._create_temp_config(content)
        try:
            with self.assertRaises(ConfigError) as ctx:
                parse_config_file(filepath)
            self.assertIn("out of bounds", str(ctx.exception))
        finally:
            os.remove(filepath)

    def test_entry_equals_exit(self) -> None:
        """Test that entry and exit having identical coords raise error."""
        content = (
            "WIDTH=10\n"
            "HEIGHT=10\n"
            "ENTRY=2,2\n"
            "EXIT=2,2\n"
            "OUTPUT_FILE=maze.txt\n"
            "PERFECT=True\n"
        )
        filepath = self._create_temp_config(content)
        try:
            with self.assertRaises(ConfigError) as ctx:
                parse_config_file(filepath)
            self.assertIn("must be different", str(ctx.exception))
        finally:
            os.remove(filepath)

    def test_invalid_boolean(self) -> None:
        """Test that invalid boolean string raises ConfigError."""
        content = (
            "WIDTH=10\n"
            "HEIGHT=10\n"
            "ENTRY=0,0\n"
            "EXIT=9,9\n"
            "OUTPUT_FILE=maze.txt\n"
            "PERFECT=Maybe\n"
        )
        filepath = self._create_temp_config(content)
        try:
            with self.assertRaises(ConfigError) as ctx:
                parse_config_file(filepath)
            self.assertIn("Invalid boolean", str(ctx.exception))
        finally:
            os.remove(filepath)

    def test_file_not_found(self) -> None:
        """Test that nonexistent file raises ConfigError."""
        with self.assertRaises(ConfigError) as ctx:
            parse_config_file("nonexistent_file_path_xyz.txt")
        self.assertIn("not found", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
