"""Tests for configuration parser and validator."""

from pathlib import Path
import pytest
from mazegen.config import (
    Config,
    ConfigFileNotFoundError,
    ConfigSyntaxError,
    ConfigValueError,
    parse_config,
)


def test_parse_valid_default_config() -> None:
    """Test parsing the default repository config.txt."""
    cfg = parse_config("config.txt")
    assert isinstance(cfg, Config)
    assert cfg.width == 20
    assert cfg.height == 15
    assert cfg.entry == (0, 0)
    assert cfg.exit == (19, 14)
    assert cfg.output_file == "maze.txt"
    assert cfg.perfect is True
    assert cfg.seed == 42


def test_parse_custom_valid(tmp_path: Path) -> None:
    """Test parsing custom valid parameters with comments and whitespace."""
    content = """
    # This is a comment
    WIDTH = 10
    HEIGHT = 8

    # Another comment
    ENTRY = 1,2
    EXIT = 9,7
    OUTPUT_FILE = test_out.txt
    PERFECT = False
    SEED = 999
    CUSTOM_KEY = hello_world
    """
    cfg_path = tmp_path / "custom.txt"
    cfg_path.write_text(content, encoding="utf-8")

    cfg = parse_config(cfg_path)
    assert cfg.width == 10
    assert cfg.height == 8
    assert cfg.entry == (1, 2)
    assert cfg.exit == (9, 7)
    assert cfg.output_file == "test_out.txt"
    assert cfg.perfect is False
    assert cfg.seed == 999
    assert cfg.extra.get("CUSTOM_KEY") == "hello_world"


def test_file_not_found() -> None:
    """Test that missing file raises ConfigFileNotFoundError."""
    with pytest.raises(ConfigFileNotFoundError) as exc_info:
        parse_config("non_existent_file_xyz.txt")
    assert "not found" in str(exc_info.value).lower()


def test_syntax_error_no_equal(tmp_path: Path) -> None:
    """Test that line without '=' raises ConfigSyntaxError."""
    cfg_path = tmp_path / "bad_syntax.txt"
    cfg_path.write_text("WIDTH 20\nHEIGHT=10\n", encoding="utf-8")
    with pytest.raises(ConfigSyntaxError) as exc_info:
        parse_config(cfg_path)
    assert "missing '='" in str(exc_info.value).lower()


def test_syntax_error_empty_key(tmp_path: Path) -> None:
    """Test that empty key raises ConfigSyntaxError."""
    cfg_path = tmp_path / "empty_key.txt"
    cfg_path.write_text("=20\n", encoding="utf-8")
    with pytest.raises(ConfigSyntaxError):
        parse_config(cfg_path)


def test_missing_mandatory_keys(tmp_path: Path) -> None:
    """Test that missing mandatory key raises ConfigValueError."""
    cfg_path = tmp_path / "missing_key.txt"
    cfg_path.write_text("WIDTH=20\nHEIGHT=15\n", encoding="utf-8")
    with pytest.raises(ConfigValueError) as exc_info:
        parse_config(cfg_path)
    assert "missing mandatory configuration key" in str(exc_info.value).lower()


def test_invalid_dimensions(tmp_path: Path) -> None:
    """Test dimensions lower than minimum boundary."""
    base_content = (
        "WIDTH=2\nHEIGHT=15\nENTRY=0,0\nEXIT=1,1\n"
        "OUTPUT_FILE=m.txt\nPERFECT=True\n"
    )
    cfg_path = tmp_path / "dim.txt"
    cfg_path.write_text(base_content, encoding="utf-8")
    with pytest.raises(ConfigValueError) as exc_info:
        parse_config(cfg_path)
    assert "must be at least 3" in str(exc_info.value)


def test_coordinates_out_of_bounds(tmp_path: Path) -> None:
    """Test entry or exit exceeding dimensions."""
    content = (
        "WIDTH=10\nHEIGHT=10\nENTRY=10,0\nEXIT=5,5\n"
        "OUTPUT_FILE=m.txt\nPERFECT=True\n"
    )
    cfg_path = tmp_path / "bounds.txt"
    cfg_path.write_text(content, encoding="utf-8")
    with pytest.raises(ConfigValueError) as exc_info:
        parse_config(cfg_path)
    assert "out of maze bounds" in str(exc_info.value)


def test_entry_equals_exit(tmp_path: Path) -> None:
    """Test entry and exit on identical cell."""
    content = (
        "WIDTH=10\nHEIGHT=10\nENTRY=2,2\nEXIT=2,2\n"
        "OUTPUT_FILE=m.txt\nPERFECT=True\n"
    )
    cfg_path = tmp_path / "same.txt"
    cfg_path.write_text(content, encoding="utf-8")
    with pytest.raises(ConfigValueError) as exc_info:
        parse_config(cfg_path)
    assert "must be different cells" in str(exc_info.value)


def test_invalid_boolean(tmp_path: Path) -> None:
    """Test invalid PERFECT boolean string."""
    content = (
        "WIDTH=10\nHEIGHT=10\nENTRY=0,0\nEXIT=1,1\n"
        "OUTPUT_FILE=m.txt\nPERFECT=Maybe\n"
    )
    cfg_path = tmp_path / "bool.txt"
    cfg_path.write_text(content, encoding="utf-8")
    with pytest.raises(ConfigValueError) as exc_info:
        parse_config(cfg_path)
    assert "invalid boolean value" in str(exc_info.value).lower()
