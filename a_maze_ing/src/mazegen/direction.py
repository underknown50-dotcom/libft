"""Direction enum and cardinal point mechanics for maze navigation."""

from enum import IntEnum
from typing import Tuple


class Direction(IntEnum):
    """Cardinal directions with corresponding bit values for wall encoding.

    Bit 0 (1): North
    Bit 1 (2): East
    Bit 2 (4): South
    Bit 3 (8): West
    """

    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    @property
    def opposite(self) -> "Direction":
        """Return the opposite cardinal direction."""
        if self == Direction.NORTH:
            return Direction.SOUTH
        if self == Direction.EAST:
            return Direction.WEST
        if self == Direction.SOUTH:
            return Direction.NORTH
        return Direction.EAST

    @property
    def delta(self) -> Tuple[int, int]:
        """Return (dx, dy) vector offset for this direction.

        Origin (0,0) is top-left:
        - North: y - 1
        - East:  x + 1
        - South: y + 1
        - West:  x - 1
        """
        if self == Direction.NORTH:
            return (0, -1)
        if self == Direction.EAST:
            return (1, 0)
        if self == Direction.SOUTH:
            return (0, 1)
        return (-1, 0)

    @property
    def char(self) -> str:
        """Return single-character identifier ('N', 'E', 'S', 'W')."""
        if self == Direction.NORTH:
            return "N"
        if self == Direction.EAST:
            return "E"
        if self == Direction.SOUTH:
            return "S"
        return "W"

    @classmethod
    def from_char(cls, char: str) -> "Direction":
        """Convert a character ('N', 'E', 'S', 'W') to Direction.

        Args:
            char: Single-letter direction string.

        Returns:
            Corresponding Direction enum member.

        Raises:
            ValueError: If char is not one of 'N', 'E', 'S', 'W'.
        """
        c = char.upper()
        if c == "N":
            return cls.NORTH
        if c == "E":
            return cls.EAST
        if c == "S":
            return cls.SOUTH
        if c == "W":
            return cls.WEST
        raise ValueError(f"Unknown direction character: '{char}'.")

    @classmethod
    def from_delta(cls, dx: int, dy: int) -> "Direction":
        """Determine Direction from a unit step delta (dx, dy).

        Args:
            dx: Horizontal delta (-1, 0, or 1).
            dy: Vertical delta (-1, 0, or 1).

        Returns:
            Corresponding Direction enum member.

        Raises:
            ValueError: If (dx, dy) is not a valid unit orthogonal step.
        """
        if dx == 0 and dy == -1:
            return cls.NORTH
        if dx == 1 and dy == 0:
            return cls.EAST
        if dx == 0 and dy == 1:
            return cls.SOUTH
        if dx == -1 and dy == 0:
            return cls.WEST
        raise ValueError(f"Invalid direction delta: ({dx}, {dy}).")
