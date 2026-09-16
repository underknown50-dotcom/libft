"""mazegen package.

A modular, extensible maze generation, solving, and visualization library.

Basic Usage:
    >>> from mazegen import MazeGenerator
    >>> # 1. Instantiate with custom parameters (size, entry, exit, seed)
    >>> generator = MazeGenerator(
    ...     width=20,
    ...     height=15,
    ...     entry=(0, 0),
    ...     exit_coord=(19, 14),
    ...     perfect=True,
    ...     seed=42
    ... )
    >>> # 2. Generate and access the grid structure
    >>> grid = generator.generate()
    >>> print(f"Grid size: {grid.width}x{grid.height}")
    >>> cell_0_0 = grid.get_cell(0, 0)
    >>> print(f"Cell walls bitmask: {cell_0_0.hex_char()}")
    >>>
    >>> # 3. Access the solution
    >>> solution_steps, solution_string = generator.solve()
    >>> print(f"Shortest path string: {solution_string}")
"""

from mazegen.config import (
    Config,
    ConfigError,
    ConfigFileNotFoundError,
    ConfigSyntaxError,
    ConfigValueError,
    parse_config,
)
from mazegen.direction import Direction
from mazegen.exporter import export_maze, verify_maze_file
from mazegen.generator import MazeGenerator
from mazegen.grid import Cell, Grid
from mazegen.pattern import (
    PATTERN_42,
    apply_pattern_42,
    can_fit_pattern,
)
from mazegen.solver import NoPathFoundError, solve_bfs
from mazegen.visualizer import (
    InteractiveVisualizer,
    render_ascii_grid,
)

__version__ = "1.0.0"
__all__ = [
    "__version__",
    "Config",
    "ConfigError",
    "ConfigFileNotFoundError",
    "ConfigSyntaxError",
    "ConfigValueError",
    "parse_config",
    "Direction",
    "Cell",
    "Grid",
    "PATTERN_42",
    "apply_pattern_42",
    "can_fit_pattern",
    "MazeGenerator",
    "NoPathFoundError",
    "solve_bfs",
    "render_ascii_grid",
    "InteractiveVisualizer",
    "export_maze",
    "verify_maze_file",
]
