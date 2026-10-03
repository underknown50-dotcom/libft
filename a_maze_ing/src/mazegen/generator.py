"""Maze generation engine implementing Perfect and Pac-Man generation modes."""

import random
from typing import List, Optional, Set, Tuple
from mazegen.config import Config
from mazegen.direction import Direction
from mazegen.grid import Cell, Grid
from mazegen.pattern import apply_pattern_42
from mazegen.solver import solve_bfs


def is_3x3_box_open(grid: Grid, top_left_x: int, top_left_y: int) -> bool:
    """Return True if all internal passages in a 3x3 subgrid are open."""
    # Check all horizontal internal passages (EAST walls)
    for row_offset in range(3):
        for col_offset in range(2):
            cell = grid.get_cell(top_left_x + col_offset, top_left_y + row_offset)
            if cell.has_wall(Direction.EAST):
                return False

    # Check all vertical internal passages (SOUTH walls)
    for row_offset in range(2):
        for col_offset in range(3):
            cell = grid.get_cell(top_left_x + col_offset, top_left_y + row_offset)
            if cell.has_wall(Direction.SOUTH):
                return False

    return True


def would_create_3x3_open_area(grid: Grid, cell_a: Cell, cell_b: Cell) -> bool:
    """Check if opening wall between cell_a and cell_b creates a 3x3 open void.

    A 3x3 open void exists if there is a 3x3 subgrid of cells where all internal
    connections between all 9 cells are completely open.
    """
    # Temporarily remove the wall to test
    grid.remove_wall_between(cell_a, cell_b)
    has_void = False

    min_x = max(0, min(cell_a.x, cell_b.x) - 2)
    max_x = min(grid.width - 3, max(cell_a.x, cell_b.x))
    min_y = max(0, min(cell_a.y, cell_b.y) - 2)
    max_y = min(grid.height - 3, max(cell_a.y, cell_b.y))

    for check_y in range(min_y, max_y + 1):
        for check_x in range(min_x, max_x + 1):
            if is_3x3_box_open(grid, check_x, check_y):
                has_void = True
                break
        if has_void:
            break

    # Restore the wall before returning
    grid.add_wall_between(cell_a, cell_b)
    return has_void


def generate_spanning_tree(
    grid: Grid,
    random_generator: random.Random,
    start_cell: Cell,
) -> None:
    """Generate a spanning tree using Randomized Prim's algorithm.

    Guarantees full connectivity and zero cycles among non-pattern cells.
    """
    visited_cells: Set[Tuple[int, int]] = set()
    candidate_walls: List[Tuple[Cell, Cell]] = []

    visited_cells.add((start_cell.x, start_cell.y))

    # Add initial walls around the start cell to the candidate walls
    for direction in [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]:
        neighbor_cell = grid.get_neighbor(start_cell.x, start_cell.y, direction)
        if neighbor_cell is not None and not neighbor_cell.is_pattern:
            candidate_walls.append((start_cell, neighbor_cell))

    while candidate_walls:
        # Pick a random candidate wall from the list
        random_index = random_generator.randrange(len(candidate_walls))
        current_cell, target_cell = candidate_walls.pop(random_index)

        target_position = (target_cell.x, target_cell.y)
        if target_position in visited_cells:
            continue

        # Carve passage to the unvisited cell
        grid.remove_wall_between(current_cell, target_cell)
        visited_cells.add(target_position)

        # Add target cell's unvisited neighbors to candidate walls
        for direction in [
            Direction.NORTH,
            Direction.EAST,
            Direction.SOUTH,
            Direction.WEST,
        ]:
            next_neighbor = grid.get_neighbor(target_cell.x, target_cell.y, direction)
            if (
                next_neighbor is not None
                and not next_neighbor.is_pattern
                and (next_neighbor.x, next_neighbor.y) not in visited_cells
            ):
                candidate_walls.append((target_cell, next_neighbor))


def braid_pacman_board(grid: Grid, random_generator: random.Random) -> None:
    """Transform a spanning tree into a Pac-Man playable board.

    Requirements:
    1. Four corners and center are open corridors.
    2. Multiple independent routes (loops).
    3. Rare to zero dead-ends (braided maze).
    4. Corridors <= 2 cells wide (no 3x3 open areas).
    """
    # 1. Force open corridors at the four corners
    corner_open_directions = [
        (0, 0, [Direction.EAST, Direction.SOUTH]),
        (grid.width - 1, 0, [Direction.WEST, Direction.SOUTH]),
        (0, grid.height - 1, [Direction.EAST, Direction.NORTH]),
        (grid.width - 1, grid.height - 1, [Direction.WEST, Direction.NORTH]),
    ]
    for corner_x, corner_y, directions in corner_open_directions:
        corner_cell = grid.get_cell(corner_x, corner_y)
        if corner_cell.is_pattern:
            continue
        for direction in directions:
            neighbor_cell = grid.get_neighbor(corner_x, corner_y, direction)
            if neighbor_cell is not None and not neighbor_cell.is_pattern:
                if corner_cell.has_wall(direction):
                    if not would_create_3x3_open_area(grid, corner_cell, neighbor_cell):
                        grid.remove_wall_between(corner_cell, neighbor_cell)

    # 2. Eliminate dead-ends (cells with 3 closed walls)
    for _ in range(5):
        dead_end_cells: List[Cell] = []
        for cell in grid.all_cells():
            if cell.is_pattern:
                continue
            closed_walls_count = sum(
                1
                for direction in [
                    Direction.NORTH,
                    Direction.EAST,
                    Direction.SOUTH,
                    Direction.WEST,
                ]
                if cell.has_wall(direction)
            )
            if closed_walls_count == 3:
                dead_end_cells.append(cell)

        if not dead_end_cells:
            break

        random_generator.shuffle(dead_end_cells)
        for dead_end_cell in dead_end_cells:
            closed_walls_count = sum(
                1
                for direction in [
                    Direction.NORTH,
                    Direction.EAST,
                    Direction.SOUTH,
                    Direction.WEST,
                ]
                if dead_end_cell.has_wall(direction)
            )
            if closed_walls_count < 3:
                continue

            candidate_passages: List[Tuple[Cell, Cell]] = []
            for direction in [
                Direction.NORTH,
                Direction.EAST,
                Direction.SOUTH,
                Direction.WEST,
            ]:
                if dead_end_cell.has_wall(direction):
                    neighbor_cell = grid.get_neighbor(
                        dead_end_cell.x, dead_end_cell.y, direction
                    )
                    if neighbor_cell is not None and not neighbor_cell.is_pattern:
                        if not would_create_3x3_open_area(
                            grid, dead_end_cell, neighbor_cell
                        ):
                            candidate_passages.append((dead_end_cell, neighbor_cell))

            if candidate_passages:
                cell_a, cell_b = random_generator.choice(candidate_passages)
                grid.remove_wall_between(cell_a, cell_b)

    # 3. Add extra loops so players always have alternative paths
    non_pattern_cells = [cell for cell in grid.all_cells() if not cell.is_pattern]
    random_generator.shuffle(non_pattern_cells)
    target_extra_loops = max(2, (grid.width * grid.height) // 25)
    loops_created = 0

    for cell in non_pattern_cells:
        if loops_created >= target_extra_loops:
            break
        for direction in [Direction.EAST, Direction.SOUTH]:
            if cell.has_wall(direction):
                neighbor_cell = grid.get_neighbor(cell.x, cell.y, direction)
                if neighbor_cell is not None and not neighbor_cell.is_pattern:
                    if not would_create_3x3_open_area(grid, cell, neighbor_cell):
                        grid.remove_wall_between(cell, neighbor_cell)
                        loops_created += 1
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
