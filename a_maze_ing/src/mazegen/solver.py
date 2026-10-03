"""Pathfinding solver implementing Breadth-First Search (BFS) for shortest path."""

from collections import deque
from typing import Dict, List, Tuple
from mazegen.direction import Direction
from mazegen.grid import Grid


class NoPathFoundError(Exception):
    """Raised when no valid path exists between entry and exit."""

    pass


def reconstruct_shortest_path(
    parent_tracker: Dict[Tuple[int, int], Tuple[Tuple[int, int], str]],
    entry: Tuple[int, int],
    exit_coord: Tuple[int, int],
) -> Tuple[List[Tuple[int, int]], str]:
    """Reconstruct path coordinates and directional string backwards.

    Traces from exit back to entry using the parent tracker.
    """
    path_coordinates: List[Tuple[int, int]] = [exit_coord]
    movement_characters: List[str] = []
    current_position = exit_coord

    while current_position != entry:
        previous_position, movement_char = parent_tracker[current_position]
        path_coordinates.append(previous_position)
        movement_characters.append(movement_char)
        current_position = previous_position

    path_coordinates.reverse()
    movement_characters.reverse()
    return path_coordinates, "".join(movement_characters)


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

    exploration_queue: deque[Tuple[int, int]] = deque([entry])
    visited_positions: set[Tuple[int, int]] = {entry}
    # parent_tracker maps: neighbor_position -> (previous_position, direction_character)
    parent_tracker: Dict[Tuple[int, int], Tuple[Tuple[int, int], str]] = {}

    destination_found = False
    while exploration_queue:
        current_x, current_y = exploration_queue.popleft()
        if (current_x, current_y) == exit_coord:
            destination_found = True
            break

        current_cell = grid.get_cell(current_x, current_y)
        for step_direction in [
            Direction.NORTH,
            Direction.EAST,
            Direction.SOUTH,
            Direction.WEST,
        ]:
            if not current_cell.has_wall(step_direction):
                neighbor_cell = grid.get_neighbor(
                    current_x, current_y, step_direction
                )
                if neighbor_cell is not None and not neighbor_cell.is_pattern:
                    neighbor_position = (neighbor_cell.x, neighbor_cell.y)
                    if neighbor_position not in visited_positions:
                        visited_positions.add(neighbor_position)
                        parent_tracker[neighbor_position] = (
                            (current_x, current_y),
                            step_direction.char,
                        )
                        exploration_queue.append(neighbor_position)

    if not destination_found:
        raise NoPathFoundError(
            f"No valid path exists between entry {entry} and exit {exit_coord}."
        )

    return reconstruct_shortest_path(parent_tracker, entry, exit_coord)
