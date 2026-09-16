"""Pathfinding solver implementing Breadth-First Search (BFS) for shortest path."""

from collections import deque
from typing import Dict, List, Tuple
from mazegen.direction import Direction
from mazegen.grid import Grid


class NoPathFoundError(Exception):
    """Raised when no valid path exists between entry and exit."""

    pass


def solve_bfs(
    grid: Grid, entry: Tuple[int, int], exit_coord: Tuple[int, int]
) -> Tuple[List[Tuple[int, int]], str]:
    """Find the shortest valid path from entry to exit using Breadth-First Search.

    Args:
        grid: The maze grid to solve.
        entry: (x, y) start coordinates.
        exit_coord: (x, y) destination coordinates.

    Returns:
        Tuple of:
        - List of (x, y) coordinates from entry to exit (inclusive).
        - String of cardinal directions ('N', 'E', 'S', 'W') connecting each step.

    Raises:
        IndexError: If entry or exit coordinates are outside grid boundaries.
        NoPathFoundError: If no walkable path connects entry and exit.
    """
    if not grid.in_bounds(*entry):
        raise IndexError(f"Entry coordinates {entry} are out of grid bounds.")
    if not grid.in_bounds(*exit_coord):
        raise IndexError(f"Exit coordinates {exit_coord} are out of grid bounds.")

    if entry == exit_coord:
        return [entry], ""

    start_cell = grid.get_cell(*entry)
    end_cell = grid.get_cell(*exit_coord)
    if start_cell.is_pattern or end_cell.is_pattern:
        raise NoPathFoundError("Entry or exit point falls on a solid pattern cell.")

    queue: deque[Tuple[int, int]] = deque([entry])
    visited: set[Tuple[int, int]] = {entry}
    # parent maps: current_pos -> (previous_pos, direction_taken)
    parent: Dict[Tuple[int, int], Tuple[Tuple[int, int], str]] = {}

    found = False
    while queue:
        cx, cy = queue.popleft()
        if (cx, cy) == exit_coord:
            found = True
            break

        current_cell = grid.get_cell(cx, cy)
        for d in [
            Direction.NORTH,
            Direction.EAST,
            Direction.SOUTH,
            Direction.WEST,
        ]:
            if not current_cell.has_wall(d):
                nbr = grid.get_neighbor(cx, cy, d)
                if nbr is not None and not nbr.is_pattern:
                    pos = (nbr.x, nbr.y)
                    if pos not in visited:
                        visited.add(pos)
                        parent[pos] = ((cx, cy), d.char)
                        queue.append(pos)

    if not found:
        raise NoPathFoundError(
            f"No valid path exists between entry {entry} and exit {exit_coord}."
        )

    # Reconstruct path backwards from exit to entry
    path_coords: List[Tuple[int, int]] = [exit_coord]
    path_dirs: List[str] = []
    curr = exit_coord

    while curr != entry:
        prev_pos, move_char = parent[curr]
        path_coords.append(prev_pos)
        path_dirs.append(move_char)
        curr = prev_pos

    path_coords.reverse()
    path_dirs.reverse()

    return path_coords, "".join(path_dirs)
