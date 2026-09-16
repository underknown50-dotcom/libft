"""Maze generation engine implementing Perfect and Pac-Man generation modes."""

import random
from typing import List, Optional, Set, Tuple
from mazegen.config import Config
from mazegen.direction import Direction
from mazegen.grid import Cell, Grid
from mazegen.pattern import apply_pattern_42
from mazegen.solver import solve_bfs


def would_create_3x3_open_area(grid: Grid, cell_a: Cell, cell_b: Cell) -> bool:
    """Check if opening wall between cell_a and cell_b creates a 3x3 open void.

    A 3x3 open void exists if there is a 3x3 subgrid of cells where all internal
    connections between all 9 cells are completely open.

    Args:
        grid: The maze grid.
        cell_a: First cell.
        cell_b: Second cell.

    Returns:
        True if opening wall would create a 3x3 open void, False otherwise.
    """
    # Temporarily open wall
    grid.remove_wall_between(cell_a, cell_b)
    has_void = False

    # Check all possible 3x3 top-left corners that could cover cell_a or cell_b
    min_x = max(0, min(cell_a.x, cell_b.x) - 2)
    max_x = min(grid.width - 3, max(cell_a.x, cell_b.x))
    min_y = max(0, min(cell_a.y, cell_b.y) - 2)
    max_y = min(grid.height - 3, max(cell_a.y, cell_b.y))

    for ty in range(min_y, max_y + 1):
        for tx in range(min_x, max_x + 1):
            box_open = True
            for dy in range(3):
                for dx in range(2):
                    c = grid.get_cell(tx + dx, ty + dy)
                    if c.has_wall(Direction.EAST):
                        box_open = False
                        break
                if not box_open:
                    break

            if box_open:
                for dy in range(2):
                    for dx in range(3):
                        c = grid.get_cell(tx + dx, ty + dy)
                        if c.has_wall(Direction.SOUTH):
                            box_open = False
                            break
                    if not box_open:
                        break

            if box_open:
                has_void = True
                break
        if has_void:
            break

    # Restore wall
    grid.add_wall_between(cell_a, cell_b)
    return has_void


def generate_spanning_tree(
    grid: Grid,
    rng: random.Random,
    start_cell: Cell,
) -> None:
    """Generate spanning tree using Randomized Prim's algorithm.

    Guarantees full connectivity and zero cycles among non-pattern cells.

    Args:
        grid: Target maze grid.
        rng: Seeded random number generator.
        start_cell: Initial cell to begin spanning tree growth.
    """
    visited: Set[Tuple[int, int]] = set()
    frontier: List[Tuple[Cell, Cell]] = []

    visited.add((start_cell.x, start_cell.y))

    for d in [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]:
        neighbor = grid.get_neighbor(start_cell.x, start_cell.y, d)
        if neighbor is not None and not neighbor.is_pattern:
            frontier.append((start_cell, neighbor))

    while frontier:
        idx = rng.randrange(len(frontier))
        c_from, c_to = frontier.pop(idx)

        pos_to = (c_to.x, c_to.y)
        if pos_to in visited:
            continue

        grid.remove_wall_between(c_from, c_to)
        visited.add(pos_to)

        for d in [
            Direction.NORTH,
            Direction.EAST,
            Direction.SOUTH,
            Direction.WEST,
        ]:
            next_neighbor = grid.get_neighbor(c_to.x, c_to.y, d)
            if (
                next_neighbor is not None
                and not next_neighbor.is_pattern
                and (next_neighbor.x, next_neighbor.y) not in visited
            ):
                frontier.append((c_to, next_neighbor))


def braid_pacman_board(grid: Grid, rng: random.Random) -> None:
    """Transform a spanning tree into a Pac-Man playable board.

    Requirements:
    1. Four corners and center are open corridors.
    2. Multiple independent routes (loops).
    3. Rare to zero dead-ends (braided maze).
    4. Corridors <= 2 cells wide (no 3x3 open areas).

    Args:
        grid: Maze grid initialized with a spanning tree.
        rng: Seeded random number generator.
    """
    corners = [
        (0, 0, [Direction.EAST, Direction.SOUTH]),
        (grid.width - 1, 0, [Direction.WEST, Direction.SOUTH]),
        (0, grid.height - 1, [Direction.EAST, Direction.NORTH]),
        (grid.width - 1, grid.height - 1, [Direction.WEST, Direction.NORTH]),
    ]
    for cx, cy, dirs in corners:
        cell = grid.get_cell(cx, cy)
        if cell.is_pattern:
            continue
        for d in dirs:
            nbr = grid.get_neighbor(cx, cy, d)
            if nbr is not None and not nbr.is_pattern:
                if cell.has_wall(d):
                    if not would_create_3x3_open_area(grid, cell, nbr):
                        grid.remove_wall_between(cell, nbr)

    for _ in range(5):
        dead_ends: List[Cell] = []
        for cell in grid.all_cells():
            if cell.is_pattern:
                continue
            closed_count = sum(
                1
                for d in [
                    Direction.NORTH,
                    Direction.EAST,
                    Direction.SOUTH,
                    Direction.WEST,
                ]
                if cell.has_wall(d)
            )
            if closed_count == 3:
                dead_ends.append(cell)

        if not dead_ends:
            break

        rng.shuffle(dead_ends)
        for cell in dead_ends:
            closed_count = sum(
                1
                for d in [
                    Direction.NORTH,
                    Direction.EAST,
                    Direction.SOUTH,
                    Direction.WEST,
                ]
                if cell.has_wall(d)
            )
            if closed_count < 3:
                continue

            candidates: List[Tuple[Cell, Cell]] = []
            for d in [
                Direction.NORTH,
                Direction.EAST,
                Direction.SOUTH,
                Direction.WEST,
            ]:
                if cell.has_wall(d):
                    nbr = grid.get_neighbor(cell.x, cell.y, d)
                    if nbr is not None and not nbr.is_pattern:
                        if not would_create_3x3_open_area(grid, cell, nbr):
                            candidates.append((cell, nbr))

            if candidates:
                chosen_a, chosen_b = rng.choice(candidates)
                grid.remove_wall_between(chosen_a, chosen_b)

    non_pattern_cells = [c for c in grid.all_cells() if not c.is_pattern]
    rng.shuffle(non_pattern_cells)
    extra_loops_target = max(2, (grid.width * grid.height) // 25)
    loops_added = 0

    for cell in non_pattern_cells:
        if loops_added >= extra_loops_target:
            break
        for d in [Direction.EAST, Direction.SOUTH]:
            if cell.has_wall(d):
                nbr = grid.get_neighbor(cell.x, cell.y, d)
                if nbr is not None and not nbr.is_pattern:
                    if not would_create_3x3_open_area(grid, cell, nbr):
                        grid.remove_wall_between(cell, nbr)
                        loops_added += 1
                        break


class MazeGenerator:
    """Reusable standalone maze generator class adhering to 42 requirements."""

    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit_coord: Tuple[int, int],
        perfect: bool = False,
        seed: Optional[int] = None,
    ) -> None:
        """Initialize the maze generator.

        Args:
            width: Maze width in cells (>= 3).
            height: Maze height in cells (>= 3).
            entry: (x, y) coordinates of entry point.
            exit_coord: (x, y) coordinates of exit point.
            perfect: True for single-path maze, False for Pac-Man playable board.
            seed: Optional random seed for reproducible generation.
        """
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit_coord
        self.perfect = perfect
        self.seed = seed
        self.grid: Optional[Grid] = None

    @classmethod
    def from_config(cls, config: Config) -> "MazeGenerator":
        """Instantiate generator directly from a validated Config object."""
        return cls(
            width=config.width,
            height=config.height,
            entry=config.entry,
            exit_coord=config.exit,
            perfect=config.perfect,
            seed=config.seed,
        )

    def generate(self) -> Grid:
        """Generate the maze according to configured mode and constraints.

        Returns:
            Fully generated, validated, and coherent Grid instance.
        """
        rng = random.Random(self.seed)
        grid = Grid(self.width, self.height)

        # 1. Embed '42' pattern first
        apply_pattern_42(grid, self.entry, self.exit)

        # 2. Find starting cell for spanning tree
        start_cell = grid.get_cell(self.entry[0], self.entry[1])
        if start_cell.is_pattern:
            for c in grid.all_cells():
                if not c.is_pattern:
                    start_cell = c
                    break

        # 3. Generate baseline spanning tree (Randomized Prim's)
        generate_spanning_tree(grid, rng, start_cell)

        # 4. If PERFECT=False, apply Pac-Man braiding and loops
        if not self.perfect:
            braid_pacman_board(grid, rng)

        self.grid = grid
        return grid

    def get_grid(self) -> Grid:
        """Return generated grid, generating on-demand if not already created."""
        if self.grid is None:
            return self.generate()
        return self.grid

    def solve(self) -> Tuple[List[Tuple[int, int]], str]:
        """Solve the maze finding the shortest path from entry to exit.

        Returns:
            Tuple of (list of path coordinates, directional string 'NESW...').
        """
        grid = self.get_grid()
        return solve_bfs(grid, self.entry, self.exit)

    def get_solution(self) -> str:
        """Return the shortest solution path as a directional string ('NESW...')."""
        _, dir_str = self.solve()
        return dir_str

    def get_solution_path(self) -> List[Tuple[int, int]]:
        """Return the shortest solution path as a sequence of (x, y) coordinates."""
        coords, _ = self.solve()
        return coords
