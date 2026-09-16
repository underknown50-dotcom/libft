"""Output file exporter and verification tools conforming to Chapter 4.5."""

from pathlib import Path
from typing import List, Tuple
from mazegen.direction import Direction
from mazegen.grid import Grid


def export_maze(
    filepath: str | Path,
    grid: Grid,
    entry: Tuple[int, int],
    exit_coord: Tuple[int, int],
    solution_str: str,
) -> None:
    """Write the maze and solution to a text file in Chapter 4.5 format.

    Format:
    - Hexadecimal rows (one per line).
    - Empty line.
    - Entry coordinates (x,y).
    - Exit coordinates (x,y).
    - Shortest path directional string ('N', 'E', 'S', 'W').
    - All lines end with newline ('\\n').

    Args:
        filepath: Destination file path.
        grid: Generated Grid instance.
        entry: (x, y) start coordinates.
        exit_coord: (x, y) destination coordinates.
        solution_str: Path string composed of [NESW] characters.

    Raises:
        OSError: If destination cannot be opened or written to.
    """
    path = Path(filepath)
    hex_lines = grid.to_hex_lines()

    lines: List[str] = []
    lines.extend(hex_lines)
    lines.append("")  # Empty line separator
    lines.append(f"{entry[0]},{entry[1]}")
    lines.append(f"{exit_coord[0]},{exit_coord[1]}")
    lines.append(solution_str)

    content = "\n".join(lines) + "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def verify_maze_file(
    filepath: str | Path,
) -> Tuple[bool, Grid, Tuple[int, int], Tuple[int, int], str, str]:
    """Parse and audit a maze output file against Chapter 4.5 requirements.

    Returns:
        Tuple of (is_valid, grid, entry, exit, solution_str, error_message).
    """
    path = Path(filepath)
    dummy_grid = Grid(3, 3)
    dummy_pt = (0, 0)

    if not path.is_file():
        return (
            False,
            dummy_grid,
            dummy_pt,
            dummy_pt,
            "",
            f"File not found: '{filepath}'",
        )

    with open(path, "r", encoding="utf-8") as f:
        raw_content = f.read()

    lines = raw_content.splitlines()
    if len(lines) < 4:
        return (
            False,
            dummy_grid,
            dummy_pt,
            dummy_pt,
            "",
            "File too short for maze specification.",
        )

    try:
        empty_idx = lines.index("")
    except ValueError:
        return (
            False,
            dummy_grid,
            dummy_pt,
            dummy_pt,
            "",
            "Missing empty separator line in file.",
        )

    hex_lines = lines[:empty_idx]
    tail = lines[empty_idx + 1 :]

    if len(tail) != 3:
        return (
            False,
            dummy_grid,
            dummy_pt,
            dummy_pt,
            "",
            f"Expected 3 tail lines (entry, exit, path), got {len(tail)}.",
        )

    entry_str, exit_str, sol_str = tail

    try:
        grid = Grid.from_hex_lines(hex_lines)
    except ValueError as err:
        return False, dummy_grid, dummy_pt, dummy_pt, "", f"Invalid hex grid: {err}"

    # Verify coherence
    coherent, err_msg = grid.is_coherent()
    if not coherent:
        return False, grid, dummy_pt, dummy_pt, "", f"Coherence failure: {err_msg}"

    # Parse coordinates
    try:
        ep = [int(p.strip()) for p in entry_str.split(",")]
        xp = [int(p.strip()) for p in exit_str.split(",")]
        entry = (ep[0], ep[1])
        exit_coord = (xp[0], xp[1])
    except Exception as err:
        return False, grid, dummy_pt, dummy_pt, "", f"Malformed coordinates: {err}"

    if not grid.in_bounds(*entry) or not grid.in_bounds(*exit_coord):
        return (
            False,
            grid,
            entry,
            exit_coord,
            sol_str,
            "Coordinates out of bounds.",
        )

    # Validate path moves through open walls
    curr = entry
    for char in sol_str:
        try:
            d = Direction.from_char(char)
        except ValueError:
            return (
                False,
                grid,
                entry,
                exit_coord,
                sol_str,
                f"Invalid direction char: '{char}'.",
            )

        cell = grid.get_cell(*curr)
        if cell.has_wall(d):
            return (
                False,
                grid,
                entry,
                exit_coord,
                sol_str,
                f"Path violates wall at {curr} moving {char}.",
            )
        dx, dy = d.delta
        curr = (curr[0] + dx, curr[1] + dy)

    if curr != exit_coord:
        return (
            False,
            grid,
            entry,
            exit_coord,
            sol_str,
            f"Path ended at {curr} instead of destination {exit_coord}.",
        )

    return True, grid, entry, exit_coord, sol_str, "Valid"
