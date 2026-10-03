"""Configuration parser and validator for A-Maze-ing."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional, Tuple


class ConfigError(Exception):
    """Base exception for all configuration errors."""

    pass


class ConfigFileNotFoundError(ConfigError):
    """Raised when the configuration file does not exist or cannot be read."""

    pass


class ConfigSyntaxError(ConfigError):
    """Raised when the configuration file contains invalid syntax."""

    pass


class ConfigValueError(ConfigError):
    """Raised when a configuration value is invalid or out of bounds."""

    pass


@dataclass(frozen=True)
class Config:
    """Validated configuration for maze generation.

    Attributes:
        width: Maze width in number of cells (must be >= 3).
        height: Maze height in number of cells (must be >= 3).
        entry: (x, y) coordinates of entry point (0-indexed).
        exit: (x, y) coordinates of exit point (0-indexed).
        output_file: Target path where the generated maze will be saved.
        perfect: Whether to generate a perfect maze (single path) or Pac-Man board.
        seed: Optional integer or string seed for reproducibility.
        extra: Additional key-value pairs parsed from the config.
    """

    width: int
    height: int
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int] = None
    extra: Dict[str, str] = field(default_factory=dict)


def _parse_coord(
    val: str, key_name: str, width: int, height: int
) -> Tuple[int, int]:
    """Parse and validate a coordinate string formatted as 'x,y'.

    Args:
        val: Coordinate string in 'x,y' format.
        key_name: Name of key for informative error message.
        width: Maze width for boundary checking.
        height: Maze height for boundary checking.

    Returns:
        Tuple of (x, y) integers.

    Raises:
        ConfigValueError: If coordinate format or boundaries are invalid.
    """
    parts = [p.strip() for p in val.split(",")]
    if len(parts) != 2:
        raise ConfigValueError(
            f"Invalid format for {key_name}: '{val}'. Expected 'x,y' (e.g. 0,0)."
        )

    try:
        x = int(parts[0])
        y = int(parts[1])
    except ValueError:
        raise ConfigValueError(
            f"{key_name} coordinates must be integers, got: '{val}'."
        )

    if x < 0 or x >= width or y < 0 or y >= height:
        raise ConfigValueError(
            f"{key_name} ({x},{y}) is out of maze bounds: "
            f"[0..{width - 1}, 0..{height - 1}]."
        )

    return x, y


def _parse_bool(val: str, key_name: str) -> bool:
    """Parse a boolean value from text.

    Args:
        val: String representation of boolean.
        key_name: Key name for error context.

    Returns:
        Parsed boolean value.

    Raises:
        ConfigValueError: If value cannot be interpreted as boolean.
    """
    lower = val.strip().lower()
    if lower in ("true", "1", "yes", "on"):
        return True
    if lower in ("false", "0", "no", "off"):
        return False
    raise ConfigValueError(
        f"Invalid boolean value for {key_name}: '{val}'. Expected 'True' or 'False'."
    )


def parse_config(filepath: str | Path) -> Config:
    """Parse and validate a configuration file.

    Args:
        filepath: Path to the configuration file.

    Returns:
        A validated Config dataclass instance.

    Raises:
        ConfigFileNotFoundError: If the file does not exist or is not readable.
        ConfigSyntaxError: If the file contains malformed lines.
        ConfigValueError: If values violate domain rules or boundaries.
    """
    path = Path(filepath)
    if not path.is_file():
        raise ConfigFileNotFoundError(f"Configuration file not found: '{filepath}'")

    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except OSError as err:
        raise ConfigFileNotFoundError(
            f"Error reading configuration file '{filepath}': {err}"
        )

    raw_pairs: Dict[str, str] = {}
    for line_num, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            raise ConfigSyntaxError(
                f"Syntax error at line {line_num}: Missing '=' delimiter in '{line}'."
            )

        key, val = line.split("=", 1)
        key = key.strip()
        val = val.strip()

        if not key:
            raise ConfigSyntaxError(
                f"Syntax error at line {line_num}: Key cannot be empty."
            )

        raw_pairs[key] = val

    mandatory_keys = [
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    ]
    missing = [k for k in mandatory_keys if k not in raw_pairs]
    if missing:
        raise ConfigValueError(
            f"Missing mandatory configuration key(s): {', '.join(missing)}"
        )

    # Parse WIDTH and HEIGHT
    try:
        width = int(raw_pairs["WIDTH"])
    except ValueError:
        raise ConfigValueError(
            f"WIDTH must be an integer, got: '{raw_pairs['WIDTH']}'."
        )

    try:
        height = int(raw_pairs["HEIGHT"])
    except ValueError:
        raise ConfigValueError(
            f"HEIGHT must be an integer, got: '{raw_pairs['HEIGHT']}'."
        )

    if width < 3:
        raise ConfigValueError(f"WIDTH must be at least 3, got: {width}.")
    if height < 3:
        raise ConfigValueError(f"HEIGHT must be at least 3, got: {height}.")

    # Parse ENTRY and EXIT
    entry = _parse_coord(raw_pairs["ENTRY"], "ENTRY", width, height)
    exit_coord = _parse_coord(raw_pairs["EXIT"], "EXIT", width, height)

    if entry == exit_coord:
        raise ConfigValueError(
            f"ENTRY and EXIT must be different cells. Got both at "
            f"({entry[0]},{entry[1]})."
        )

    # Parse OUTPUT_FILE
    output_file = raw_pairs["OUTPUT_FILE"]
    if not output_file:
        raise ConfigValueError("OUTPUT_FILE cannot be empty.")

    # Parse PERFECT
    perfect = _parse_bool(raw_pairs["PERFECT"], "PERFECT")

    # Parse optional SEED
    seed: Optional[int] = None
    if "SEED" in raw_pairs and raw_pairs["SEED"]:
        try:
            seed = int(raw_pairs["SEED"])
        except ValueError:
            # Fallback to string hash if seed is non-integer string
            seed = hash(raw_pairs["SEED"])

    # Extra options
    extra: Dict[str, str] = {
        k: v
        for k, v in raw_pairs.items()
        if k not in mandatory_keys and k != "SEED"
    }

    return Config(
        width=width,
        height=height,
        entry=entry,
        exit=exit_coord,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
        extra=extra,
    )
