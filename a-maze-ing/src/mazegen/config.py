"""Configuration parser and validator for the maze generator.

This module handles reading KEY=VALUE configuration files, validating
mandatory and optional parameters according to 42 subject requirements,
and providing structured configuration objects with graceful error handling.
"""

from dataclasses import dataclass
from typing import Optional, Tuple


class ConfigError(Exception):
    """Exception raised for errors in the configuration file or parameters."""

    pass


@dataclass(frozen=True)
class MazeConfig:
    """Immutable data container for validated maze generation configuration.

    Attributes:
        width: Number of cells horizontally (x axis).
        height: Number of cells vertically (y axis).
        entry: Tuple of (x, y) coordinates for the maze entrance.
        exit: Tuple of (x, y) coordinates for the maze exit.
        output_file: Destination filepath where the maze will be saved.
        perfect: True for a single-path maze, False for Pac-Man board.
        seed: Optional integer seed for reproducible random generation.
    """

    width: int
    height: int
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int] = None


def _parse_coordinates(raw_value: str, key_name: str) -> Tuple[int, int]:
    """Parse and validate an x,y coordinate string.

    Args:
        raw_value: String formatted as 'x,y'.
        key_name: Configuration key name (for error messages).

    Returns:
        Tuple of (x, y) integer coordinates.

    Raises:
        ConfigError: If format is invalid or contains non-integers.
    """
    parts = [p.strip() for p in raw_value.split(",")]
    if len(parts) != 2:
        raise ConfigError(
            f"Invalid format for '{key_name}': "
            f"expected 'x,y', got '{raw_value}'"
        )
    try:
        x = int(parts[0])
        y = int(parts[1])
    except ValueError:
        raise ConfigError(
            f"Invalid coordinates for '{key_name}': "
            f"values must be integers, got '{raw_value}'"
        )
    return (x, y)


def _parse_boolean(raw_value: str, key_name: str) -> bool:
    """Parse and validate a boolean value.

    Args:
        raw_value: String representation of boolean ('True', 'False', etc.).
        key_name: Configuration key name (for error messages).

    Returns:
        Boolean value.

    Raises:
        ConfigError: If string is not a recognizable boolean.
    """
    normalized = raw_value.strip().lower()
    if normalized in ("true", "1", "yes"):
        return True
    if normalized in ("false", "0", "no"):
        return False
    raise ConfigError(
        f"Invalid boolean value for '{key_name}': "
        f"expected 'True' or 'False', got '{raw_value}'"
    )


def parse_config_file(filepath: str) -> MazeConfig:
    """Parse a configuration file and validate all parameters.

    Lines starting with '#' are treated as comments and ignored.
    Each configuration line must follow the format 'KEY=VALUE'.

    Args:
        filepath: Path to the configuration text file.

    Returns:
        A validated MazeConfig instance.

    Raises:
        ConfigError: If the file cannot be read, syntax is invalid,
            mandatory keys are missing, or parameters are out of bounds.
    """
    raw_config: dict[str, str] = {}

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            for line_number, raw_line in enumerate(file, start=1):
                line = raw_line.strip()
                # Ignore empty lines and comment lines
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ConfigError(
                        f"Syntax error at {filepath}:{line_number}: "
                        f"expected 'KEY=VALUE', got '{line}'"
                    )
                key, _, value = line.partition("=")
                key = key.strip().upper()
                value = value.strip()
                if not key:
                    raise ConfigError(
                        f"Empty key name at {filepath}:{line_number}"
                    )
                raw_config[key] = value
    except FileNotFoundError:
        raise ConfigError(f"Configuration file not found: '{filepath}'")
    except PermissionError:
        raise ConfigError(
            f"Permission denied reading configuration file: '{filepath}'"
        )
    except IsADirectoryError:
        raise ConfigError(
            f"Expected a file but found a directory: '{filepath}'"
        )
    except OSError as exc:
        raise ConfigError(
            f"Could not read configuration file '{filepath}': {exc}"
        )

    # Check for mandatory keys
    mandatory = (
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    )
    missing_keys = [k for k in mandatory if k not in raw_config]
    if missing_keys:
        raise ConfigError(
            f"Missing mandatory configuration key(s): "
            f"{', '.join(missing_keys)}"
        )

    # Validate WIDTH and HEIGHT
    try:
        width = int(raw_config["WIDTH"])
        height = int(raw_config["HEIGHT"])
    except ValueError:
        raise ConfigError("WIDTH and HEIGHT must be valid integers")

    if width < 3 or height < 3:
        raise ConfigError(
            f"Maze dimensions too small ({width}x{height}). "
            f"Minimum dimensions are 3x3"
        )

    # Validate ENTRY and EXIT coordinates
    entry = _parse_coordinates(raw_config["ENTRY"], "ENTRY")
    exit_coord = _parse_coordinates(raw_config["EXIT"], "EXIT")

    # Ensure coordinates are within grid bounds
    if not (0 <= entry[0] < width and 0 <= entry[1] < height):
        raise ConfigError(
            f"ENTRY coordinates {entry} are out of bounds for "
            f"maze size {width}x{height}"
        )
    if not (0 <= exit_coord[0] < width and 0 <= exit_coord[1] < height):
        raise ConfigError(
            f"EXIT coordinates {exit_coord} are out of bounds for "
            f"maze size {width}x{height}"
        )

    # Ensure ENTRY and EXIT are distinct
    if entry == exit_coord:
        raise ConfigError(
            f"ENTRY and EXIT coordinates must be different, both are {entry}"
        )

    # Validate PERFECT flag
    perfect = _parse_boolean(raw_config["PERFECT"], "PERFECT")

    # Validate OUTPUT_FILE
    output_file = raw_config["OUTPUT_FILE"].strip()
    if not output_file:
        raise ConfigError("OUTPUT_FILE cannot be empty")

    # Validate optional SEED if present
    seed: Optional[int] = None
    if "SEED" in raw_config:
        try:
            seed = int(raw_config["SEED"])
        except ValueError:
            raise ConfigError(
                f"SEED must be an integer, got '{raw_config['SEED']}'"
            )

    return MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit=exit_coord,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
    )
