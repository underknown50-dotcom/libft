"""Maze grid data structure, cell bitmask encoding, and coherence verification."""

from typing import Iterator, List, Optional, Tuple
from mazegen.direction import Direction


class Cell:
    """Represents a single cell in the maze grid.

    Each cell maintains a bitmask of closed walls:
    - Bit 0 (1): North
    - Bit 1 (2): East
    - Bit 2 (4): South
    - Bit 3 (8): West
    """

    def __init__(
        self, x: int, y: int, walls: int = 15, is_pattern: bool = False
    ) -> None:
        """Initialize a cell.

        Args:
            x: Column index (0 <= x < width).
            y: Row index (0 <= y < height).
            walls: Initial wall bitmask (defaults to 15, all 4 walls closed).
            is_pattern: True if this cell is part of the embedded '42' pattern.
        """
        self.x: int = x
        self.y: int = y
        self.walls: int = walls
        self.is_pattern: bool = is_pattern

    def has_wall(self, direction: Direction) -> bool:
        """Check whether a wall is closed in the given direction."""
        return bool(self.walls & direction.value)

    def open_wall(self, direction: Direction) -> None:
        """Open (remove) the wall in the specified direction."""
        self.walls &= ~direction.value

    def close_wall(self, direction: Direction) -> None:
        """Close (add) the wall in the specified direction."""
        self.walls |= direction.value

    def hex_char(self) -> str:
        """Return hex representation of the cell's wall bitmask ('0'..'F')."""
        return format(self.walls, "X")

    def __repr__(self) -> str:
        """String representation of the cell for debugging."""
        return (
            f"Cell(x={self.x}, y={self.y}, walls={self.hex_char()}, "
            f"pattern={self.is_pattern})"
        )


class Grid:
    """2D rectangular grid representing the maze.

    Coordinates:
    - (0, 0) is top-left.
    - x increases eastward: [0 .. width - 1].
    - y increases southward: [0 .. height - 1].
    """

    def __init__(self, width: int, height: int) -> None:
        """Initialize a grid of cells, all with 4 closed walls by default.

        Args:
            width: Maze width in cells (must be >= 3).
            height: Maze height in cells (must be >= 3).

        Raises:
            ValueError: If width or height is less than 3.
        """
        if width < 3 or height < 3:
            raise ValueError(
                f"Grid dimensions must be at least 3x3, got {width}x{height}."
            )

        self.width: int = width
        self.height: int = height
        self._cells: List[List[Cell]] = [
            [Cell(x, y) for x in range(width)] for y in range(height)
        ]

    def in_bounds(self, x: int, y: int) -> bool:
        """Check if coordinates (x, y) lie inside the grid boundaries."""
        return 0 <= x < self.width and 0 <= y < self.height

    def get_cell(self, x: int, y: int) -> Cell:
        """Retrieve the cell at coordinate (x, y).

        Args:
            x: Column index.
            y: Row index.

        Returns:
            The Cell instance at (x, y).

        Raises:
            IndexError: If (x, y) is out of grid boundaries.
        """
        if not self.in_bounds(x, y):
            raise IndexError(
                f"Coordinates ({x}, {y}) out of grid bounds "
                f"[0..{self.width - 1}, 0..{self.height - 1}]."
            )
        return self._cells[y][x]

    def get_neighbor(
        self, x: int, y: int, direction: Direction
    ) -> Optional[Cell]:
        """Get adjacent cell in the given cardinal direction, if in bounds.

        Args:
            x: Source column index.
            y: Source row index.
            direction: Direction towards target cell.

        Returns:
            Neighboring Cell, or None if out of bounds.
        """
        dx, dy = direction.delta
        nx, ny = x + dx, y + dy
        if self.in_bounds(nx, ny):
            return self.get_cell(nx, ny)
        return None

    def all_cells(self) -> Iterator[Cell]:
        """Yield every cell in the grid in row-major order."""
        for row in self._cells:
            for cell in row:
                yield cell

    def remove_wall_between(self, cell_a: Cell, cell_b: Cell) -> None:
        """Remove the wall shared between two adjacent cells coherently.

        Args:
            cell_a: First cell.
            cell_b: Neighboring cell.

        Raises:
            ValueError: If cell_a and cell_b are not orthogonal neighbors.
        """
        dx = cell_b.x - cell_a.x
        dy = cell_b.y - cell_a.y
        direction = Direction.from_delta(dx, dy)
        opposite = direction.opposite

        cell_a.open_wall(direction)
        cell_b.open_wall(opposite)

    def add_wall_between(self, cell_a: Cell, cell_b: Cell) -> None:
        """Add the wall shared between two adjacent cells coherently.

        Args:
            cell_a: First cell.
            cell_b: Neighboring cell.

        Raises:
            ValueError: If cell_a and cell_b are not orthogonal neighbors.
        """
        dx = cell_b.x - cell_a.x
        dy = cell_b.y - cell_a.y
        direction = Direction.from_delta(dx, dy)
        opposite = direction.opposite

        cell_a.close_wall(direction)
        cell_b.close_wall(opposite)

    def is_coherent(self) -> Tuple[bool, Optional[str]]:
        """Verify that all wall encodings in the grid are physically coherent.

        Checks:
        1. External boundaries have closed outer walls.
        2. Every shared internal wall between neighboring cells is identical
           (if East of cell A is open, West of neighbor B must be open, etc.).

        Returns:
            Tuple of (True, None) if valid, or (False, error_description) if flawed.
        """
        for y in range(self.height):
            for x in range(self.width):
                cell = self.get_cell(x, y)

                # Check North wall
                if y == 0:
                    if not cell.has_wall(Direction.NORTH):
                        return (
                            False,
                            f"Border breach: North wall at ({x},{y}) is open.",
                        )
                else:
                    n_nbr = self.get_cell(x, y - 1)
                    if cell.has_wall(Direction.NORTH) != n_nbr.has_wall(
                        Direction.SOUTH
                    ):
                        return False, (
                            f"Wall incoherence between ({x},{y}) North and "
                            f"({n_nbr.x},{n_nbr.y}) South."
                        )

                # Check South wall
                if y == self.height - 1:
                    if not cell.has_wall(Direction.SOUTH):
                        return (
                            False,
                            f"Border breach: South wall at ({x},{y}) is open.",
                        )

                # Check West wall
                if x == 0:
                    if not cell.has_wall(Direction.WEST):
                        return (
                            False,
                            f"Border breach: West wall at ({x},{y}) is open.",
                        )
                else:
                    w_nbr = self.get_cell(x - 1, y)
                    if cell.has_wall(Direction.WEST) != w_nbr.has_wall(
                        Direction.EAST
                    ):
                        return False, (
                            f"Wall incoherence between ({x},{y}) West and "
                            f"({w_nbr.x},{w_nbr.y}) East."
                        )

                # Check East wall
                if x == self.width - 1:
                    if not cell.has_wall(Direction.EAST):
                        return (
                            False,
                            f"Border breach: East wall at ({x},{y}) is open.",
                        )

        return True, None

    def to_hex_lines(self) -> List[str]:
        """Convert the entire maze grid into hexadecimal rows.

        Returns:
            List of strings (one string per row, each row of length width).
        """
        return ["".join(cell.hex_char() for cell in row) for row in self._cells]

    @classmethod
    def from_hex_lines(cls, lines: List[str]) -> "Grid":
        """Reconstruct a Grid instance from hexadecimal row strings.

        Args:
            lines: List of strings where each character is a hex digit.

        Returns:
            Reconstructed Grid instance.

        Raises:
            ValueError: If rows are empty, mismatched lengths, or invalid hex chars.
        """
        if not lines:
            raise ValueError("Hex lines list cannot be empty.")

        height = len(lines)
        width = len(lines[0])

        for line_idx, line in enumerate(lines):
            if len(line) != width:
                raise ValueError(
                    f"Row length mismatch at row {line_idx}: "
                    f"expected {width}, got {len(line)}."
                )

        grid = cls(width, height)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                try:
                    walls = int(char, 16)
                except ValueError:
                    raise ValueError(
                        f"Invalid hexadecimal digit '{char}' at ({x}, {y})."
                    )
                grid.get_cell(x, y).walls = walls

        return grid
