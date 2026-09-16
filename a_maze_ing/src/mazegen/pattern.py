"""Embedded '42' pattern generation and boundary masking."""

import sys
from typing import Optional, Set, Tuple
from mazegen.direction import Direction
from mazegen.grid import Grid

# Standard 42 bitmap: 5 rows by 7 columns
# '4' is 3x5, 1 space column, '2' is 3x5
PATTERN_42: Tuple[Tuple[int, ...], ...] = (
    (1, 0, 1, 0, 1, 1, 1),
    (1, 0, 1, 0, 0, 0, 1),
    (1, 1, 1, 0, 1, 1, 1),
    (0, 0, 1, 0, 1, 0, 0),
    (0, 0, 1, 0, 1, 1, 1),
)

PATTERN_WIDTH: int = 7
PATTERN_HEIGHT: int = 5
# Clearance of at least 1 cell on every border to maintain corridor loop around 42
MIN_MAZE_WIDTH: int = PATTERN_WIDTH + 2   # 9
MIN_MAZE_HEIGHT: int = PATTERN_HEIGHT + 2  # 7


def get_pattern_cells_at(
    start_x: int, start_y: int
) -> Set[Tuple[int, int]]:
    """Return the set of absolute grid coordinates occupied by pattern cells.

    Args:
        start_x: Top-left X coordinate where pattern begins.
        start_y: Top-left Y coordinate where pattern begins.

    Returns:
        Set of (x, y) coordinates for all cells that are part of the '42'.
    """
    pattern_cells: Set[Tuple[int, int]] = set()
    for py, row in enumerate(PATTERN_42):
        for px, val in enumerate(row):
            if val == 1:
                pattern_cells.add((start_x + px, start_y + py))
    return pattern_cells


def can_fit_pattern(
    width: int,
    height: int,
    entry: Tuple[int, int],
    exit_coord: Tuple[int, int],
) -> Tuple[bool, Optional[Tuple[int, int]], str]:
    """Check whether the '42' pattern can fit without collisions.

    Args:
        width: Maze grid width.
        height: Maze grid height.
        entry: (x, y) coordinates of entry point.
        exit_coord: (x, y) coordinates of exit point.

    Returns:
        Tuple of:
        - can_fit (bool)
        - (start_x, start_y) if can fit, else None
        - reason (str) explaining why it fits or cannot fit
    """
    if width < MIN_MAZE_WIDTH or height < MIN_MAZE_HEIGHT:
        return (
            False,
            None,
            f"Maze dimensions ({width}x{height}) too small for '42' pattern "
            f"(minimum required: {MIN_MAZE_WIDTH}x{MIN_MAZE_HEIGHT}).",
        )

    start_x = (width - PATTERN_WIDTH) // 2
    start_y = (height - PATTERN_HEIGHT) // 2

    occupied = get_pattern_cells_at(start_x, start_y)
    if entry in occupied:
        return (
            False,
            None,
            f"Pattern collision: ENTRY point {entry} overlaps with '42' pattern.",
        )
    if exit_coord in occupied:
        return (
            False,
            None,
            f"Pattern collision: EXIT point {exit_coord} overlaps with '42' pattern.",
        )

    return True, (start_x, start_y), "Pattern fits centered in grid."


def apply_pattern_42(
    grid: Grid,
    entry: Tuple[int, int],
    exit_coord: Tuple[int, int],
    verbose: bool = True,
) -> bool:
    """Embed the '42' pattern into the grid as fully closed cells.

    If the pattern cannot fit due to size constraints or entry/exit collisions,
    an error message is printed to stderr as required by the 42 subject.

    Args:
        grid: Target Grid instance.
        entry: Entry coordinates.
        exit_coord: Exit coordinates.
        verbose: If True, print informative message when pattern is omitted.

    Returns:
        True if pattern was embedded, False if omitted.
    """
    fits, offset, reason = can_fit_pattern(
        grid.width, grid.height, entry, exit_coord
    )
    if not fits or offset is None:
        if verbose:
            print(f"Notice: '42' pattern omitted: {reason}", file=sys.stderr)
        return False

    start_x, start_y = offset
    for py, row in enumerate(PATTERN_42):
        for px, val in enumerate(row):
            if val == 1:
                gx = start_x + px
                gy = start_y + py
                cell = grid.get_cell(gx, gy)
                cell.is_pattern = True
                cell.walls = 15  # Fully closed (0xF)

                # Ensure all surrounding neighbors keep walls facing this cell closed
                for d in [
                    Direction.NORTH,
                    Direction.EAST,
                    Direction.SOUTH,
                    Direction.WEST,
                ]:
                    neighbor = grid.get_neighbor(gx, gy, d)
                    if neighbor is not None:
                        neighbor.close_wall(d.opposite)

    return True
