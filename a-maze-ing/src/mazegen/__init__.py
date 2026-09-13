"""Mazegen: A reusable maze generation and pathfinding engine."""

from .config import ConfigError, MazeConfig, parse_config_file

__version__ = "1.0.0"

__all__ = [
    "ConfigError",
    "MazeConfig",
    "parse_config_file",
]
