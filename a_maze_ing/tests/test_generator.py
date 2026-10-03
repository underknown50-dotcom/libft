"""Tests for maze generation core (Perfect mode and Pac-Man mode)."""

from collections import deque
from typing import Set, Tuple
from mazegen.config import Config
from mazegen.direction import Direction
from mazegen.generator import MazeGenerator
from mazegen.grid import Grid


def _count_graph_stats(grid: Grid) -> Tuple[int, int]:
    """Calculate non-pattern vertices (V) and carved passages (E).

    Returns:
        Tuple of (V, E).
    """
    non_pattern_cells = [c for c in grid.all_cells() if not c.is_pattern]
    v = len(non_pattern_cells)

    # Count edges: each open internal wall represents one bidirectional edge
    e = 0
    for cell in non_pattern_cells:
        for d in [Direction.EAST, Direction.SOUTH]:
            if not cell.has_wall(d):
                nbr = grid.get_neighbor(cell.x, cell.y, d)
                if nbr is not None and not nbr.is_pattern:
                    e += 1
    return v, e


def _verify_full_connectivity(grid: Grid, start: Tuple[int, int]) -> bool:
    """Verify that all non-pattern cells are reachable via BFS."""
    non_pattern_cells = [c for c in grid.all_cells() if not c.is_pattern]
    visited: Set[Tuple[int, int]] = set()
    queue = deque([start])
    visited.add(start)

    while queue:
        cx, cy = queue.popleft()
        cell = grid.get_cell(cx, cy)
        for d in [
            Direction.NORTH,
            Direction.EAST,
            Direction.SOUTH,
            Direction.WEST,
        ]:
            if not cell.has_wall(d):
                nbr = grid.get_neighbor(cx, cy, d)
                if nbr is not None and not nbr.is_pattern:
                    pos = (nbr.x, nbr.y)
                    if pos not in visited:
                        visited.add(pos)
                        queue.append(pos)

    return len(visited) == len(non_pattern_cells)


def _has_any_3x3_void(grid: Grid) -> bool:
    """Audit grid for any 3x3 open void (all internal walls open)."""
    for ty in range(grid.height - 2):
        for tx in range(grid.width - 2):
            box_open = True
            for dy in range(3):
                for dx in range(2):
                    if grid.get_cell(tx + dx, ty + dy).has_wall(
                        Direction.EAST
                    ):
                        box_open = False
                        break
                if not box_open:
                    break
            if box_open:
                for dy in range(2):
                    for dx in range(3):
                        if grid.get_cell(tx + dx, ty + dy).has_wall(
                            Direction.SOUTH
                        ):
                            box_open = False
                            break
                    if not box_open:
                        break
            if box_open:
                return True
    return False


def test_perfect_maze_generation() -> None:
    """Verify PERFECT=True generates an exact spanning tree with zero loops."""
    gen = MazeGenerator(
        width=20,
        height=15,
        entry=(0, 0),
        exit_coord=(19, 14),
        perfect=True,
        seed=12345,
    )
    grid = gen.generate()

    # 1. Grid coherence
    coherent, err = grid.is_coherent()
    assert coherent is True, err

    # 2. Full connectivity
    assert _verify_full_connectivity(grid, (0, 0)) is True

    # 3. Spanning tree mathematical property: E == V - 1 (0 cycles)
    v, e = _count_graph_stats(grid)
    assert e == v - 1


def test_perfect_maze_reproducibility() -> None:
    """Verify that same seed produces identical maze in PERFECT mode."""
    gen1 = MazeGenerator(
        width=18,
        height=14,
        entry=(0, 0),
        exit_coord=(17, 13),
        perfect=True,
        seed=42,
    )
    gen2 = MazeGenerator(
        width=18,
        height=14,
        entry=(0, 0),
        exit_coord=(17, 13),
        perfect=True,
        seed=42,
    )
    assert gen1.generate().to_hex_lines() == gen2.generate().to_hex_lines()


def test_pacman_board_generation() -> None:
    """Verify PERFECT=False generates multi-loop board with rare dead-ends."""
    gen = MazeGenerator(
        width=20,
        height=15,
        entry=(0, 0),
        exit_coord=(19, 14),
        perfect=False,
        seed=12345,
    )
    grid = gen.generate()

    # 1. Grid coherence
    coherent, err = grid.is_coherent()
    assert coherent is True, err

    # 2. Full connectivity
    assert _verify_full_connectivity(grid, (0, 0)) is True

    # 3. Loops exist: E > V - 1 (at least 2 independent loops)
    v, e = _count_graph_stats(grid)
    cycles = e - v + 1
    assert cycles >= 2

    # 4. Dead-ends are rare or zero
    dead_ends = sum(
        1
        for c in grid.all_cells()
        if not c.is_pattern
        and sum(
            1
            for d in [
                Direction.NORTH,
                Direction.EAST,
                Direction.SOUTH,
                Direction.WEST,
            ]
            if c.has_wall(d)
        )
        == 3
    )
    # A couple tolerated, but should stay rare (<= 4 in a 20x15 grid)
    assert dead_ends <= 4

    # 5. No 3x3 open void exists
    assert _has_any_3x3_void(grid) is False


def test_generator_from_config() -> None:
    """Verify MazeGenerator instantiation via Config dataclass."""
    cfg = Config(
        width=16,
        height=12,
        entry=(1, 1),
        exit=(15, 11),
        output_file="out.txt",
        perfect=False,
        seed=777,
    )
    gen = MazeGenerator.from_config(cfg)
    grid = gen.get_grid()
    assert grid.width == 16
    assert grid.height == 12
    coherent, _ = grid.is_coherent()
    assert coherent is True
