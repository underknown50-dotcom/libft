"""Tests for pathfinding solver (BFS)."""

import pytest
from mazegen.direction import Direction
from mazegen.generator import MazeGenerator
from mazegen.grid import Grid
from mazegen.solver import NoPathFoundError, solve_bfs


def test_bfs_solves_perfect_maze() -> None:
    """Verify BFS finds valid path in a perfect maze."""
    gen = MazeGenerator(
        width=15,
        height=11,
        entry=(0, 0),
        exit_coord=(14, 10),
        perfect=True,
        seed=101,
    )
    coords, dir_str = gen.solve()

    assert coords[0] == (0, 0)
    assert coords[-1] == (14, 10)
    assert len(dir_str) == len(coords) - 1
    assert set(dir_str).issubset({"N", "E", "S", "W"})

    # Verify step-by-step that every move passes through an open wall
    grid = gen.get_grid()
    for i in range(len(coords) - 1):
        curr_pos = coords[i]
        next_pos = coords[i + 1]
        move_char = dir_str[i]
        direction = Direction.from_char(move_char)

        # Check coordinate delta
        dx, dy = direction.delta
        assert (curr_pos[0] + dx, curr_pos[1] + dy) == next_pos

        # Check cell walls
        cell = grid.get_cell(*curr_pos)
        assert cell.has_wall(direction) is False


def test_bfs_solves_pacman_maze() -> None:
    """Verify BFS finds valid shortest path in a multi-loop Pac-Man maze."""
    gen = MazeGenerator(
        width=20,
        height=15,
        entry=(0, 0),
        exit_coord=(19, 14),
        perfect=False,
        seed=202,
    )
    coords, dir_str = gen.solve()

    assert coords[0] == (0, 0)
    assert coords[-1] == (19, 14)
    assert len(dir_str) == len(coords) - 1

    grid = gen.get_grid()
    for i in range(len(coords) - 1):
        curr = grid.get_cell(*coords[i])
        d = Direction.from_char(dir_str[i])
        assert curr.has_wall(d) is False


def test_bfs_same_entry_and_exit() -> None:
    """Verify behavior when entry and exit are identical."""
    grid = Grid(5, 5)
    coords, dir_str = solve_bfs(grid, (2, 2), (2, 2))
    assert coords == [(2, 2)]
    assert dir_str == ""


def test_bfs_out_of_bounds() -> None:
    """Verify out-of-bounds coordinates raise IndexError."""
    grid = Grid(5, 5)
    with pytest.raises(IndexError):
        solve_bfs(grid, (-1, 0), (2, 2))
    with pytest.raises(IndexError):
        solve_bfs(grid, (0, 0), (5, 5))


def test_bfs_unreachable_destination() -> None:
    """Verify unreachable destination raises NoPathFoundError."""
    # A fresh grid has all walls closed (0xF), so cells are disconnected
    grid = Grid(5, 5)
    with pytest.raises(NoPathFoundError):
        solve_bfs(grid, (0, 0), (4, 4))


def test_generator_convenience_methods() -> None:
    """Verify get_solution and get_solution_path on MazeGenerator."""
    gen = MazeGenerator(
        width=12,
        height=10,
        entry=(0, 0),
        exit_coord=(11, 9),
        perfect=True,
        seed=303,
    )
    sol_str = gen.get_solution()
    sol_path = gen.get_solution_path()

    assert isinstance(sol_str, str)
    assert len(sol_str) > 0
    assert len(sol_path) == len(sol_str) + 1
