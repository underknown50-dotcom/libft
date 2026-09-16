"""Interactive terminal ASCII/ANSI visualizer for A-Maze-ing."""

import sys
from typing import Callable, List, Optional, Tuple
from mazegen.direction import Direction
from mazegen.generator import MazeGenerator
from mazegen.grid import Grid


# ANSI escape sequences
RESET = "\033[0m"
BOLD = "\033[1m"
COLOR_ENTRY = "\033[95m"    # Bright Magenta
COLOR_EXIT = "\033[91m"     # Bright Red
COLOR_PATH = "\033[96m"     # Bright Cyan
COLOR_PATTERN = "\033[90m"  # Bright Black / Dark Gray

WALL_PALETTE = [
    ("\033[97m", "Bright White"),
    ("\033[33m", "Warm Yellow/Olive"),
    ("\033[92m", "Emerald Green"),
    ("\033[94m", "Vibrant Blue"),
    ("\033[93m", "Golden Amber"),
    ("\033[35m", "Deep Purple"),
    ("\033[36m", "Aqua Cyan"),
]


def render_ascii_grid(
    grid: Grid,
    entry: Tuple[int, int],
    exit_coord: Tuple[int, int],
    path: Optional[List[Tuple[int, int]]] = None,
    color_index: int = 0,
    use_ansi: bool = True,
    use_unicode: Optional[bool] = None,
) -> str:
    """Render the maze grid as an ASCII/ANSI block diagram.

    Args:
        grid: The Grid instance to visualize.
        entry: (x, y) start coordinates.
        exit_coord: (x, y) destination coordinates.
        path: Optional list of (x, y) coordinates along the solution path.
        color_index: Index into WALL_PALETTE for wall coloring.
        use_ansi: If True, include ANSI color escape codes.
        use_unicode: Whether to use Unicode block characters (default: auto-detect).

    Returns:
        Formatted multi-line string ready for terminal display.
    """
    if use_unicode is None:
        enc = (getattr(sys.stdout, "encoding", "") or "").lower()
        use_unicode = enc in ("utf-8", "utf8")

    wall_color_code, _ = WALL_PALETTE[color_index % len(WALL_PALETTE)]
    c_wall = wall_color_code if use_ansi else ""
    c_entry = COLOR_ENTRY if use_ansi else ""
    c_exit = COLOR_EXIT if use_ansi else ""
    c_path = COLOR_PATH if use_ansi else ""
    c_pat = COLOR_PATTERN if use_ansi else ""
    c_rst = RESET if use_ansi else ""

    # Glyphs
    g_wall = "██" if use_unicode else "##"
    g_pat = "██" if use_unicode else "42"
    g_entry = "██" if use_unicode else "EN"
    g_exit = "██" if use_unicode else "EX"
    g_path = "██" if use_unicode else "··"

    # Canvas dimensions: (2*height + 1) rows by (2*width + 1) cols
    canvas_h = 2 * grid.height + 1
    canvas_w = 2 * grid.width + 1
    canvas = [["WALL" for _ in range(canvas_w)] for _ in range(canvas_h)]

    # 1. Carve cell interiors and open walls
    for y in range(grid.height):
        for x in range(grid.width):
            cell = grid.get_cell(x, y)
            cy, cx = 2 * y + 1, 2 * x + 1

            if cell.is_pattern:
                canvas[cy][cx] = "PATTERN"
            else:
                canvas[cy][cx] = "FLOOR"

            if not cell.has_wall(Direction.NORTH):
                canvas[cy - 1][cx] = "FLOOR"
            if not cell.has_wall(Direction.SOUTH):
                canvas[cy + 1][cx] = "FLOOR"
            if not cell.has_wall(Direction.WEST):
                canvas[cy][cx - 1] = "FLOOR"
            if not cell.has_wall(Direction.EAST):
                canvas[cy][cx + 1] = "FLOOR"

    # 2. Overlay shortest solution path if provided
    if path and len(path) > 1:
        for i in range(len(path)):
            px, py = path[i]
            canvas[2 * py + 1][2 * px + 1] = "PATH"
            if i < len(path) - 1:
                nx, ny = path[i + 1]
                mid_y = (2 * py + 1 + 2 * ny + 1) // 2
                mid_x = (2 * px + 1 + 2 * nx + 1) // 2
                canvas[mid_y][mid_x] = "PATH"

    # 3. Mark Entry and Exit points
    canvas[2 * entry[1] + 1][2 * entry[0] + 1] = "ENTRY"
    canvas[2 * exit_coord[1] + 1][2 * exit_coord[0] + 1] = "EXIT"

    # 4. Convert canvas into terminal characters
    lines: List[str] = []
    for r in range(canvas_h):
        line_chars: List[str] = []
        for c in range(canvas_w):
            val = canvas[r][c]
            if val == "WALL":
                line_chars.append(f"{c_wall}{g_wall}{c_rst}")
            elif val == "FLOOR":
                line_chars.append("  ")
            elif val == "PATTERN":
                line_chars.append(f"{c_pat}{g_pat}{c_rst}")
            elif val == "ENTRY":
                line_chars.append(f"{c_entry}{g_entry}{c_rst}")
            elif val == "EXIT":
                line_chars.append(f"{c_exit}{g_exit}{c_rst}")
            elif val == "PATH":
                line_chars.append(f"{c_path}{g_path}{c_rst}")
        lines.append("".join(line_chars))

    return "\n".join(lines)


class InteractiveVisualizer:
    """Interactive terminal visualizer conforming to Chapter 5."""

    def __init__(self, generator: MazeGenerator, use_ansi: bool = True) -> None:
        """Initialize the visualizer.

        Args:
            generator: Active MazeGenerator instance.
            use_ansi: Whether to emit ANSI color escapes.
        """
        self.generator = generator
        self.use_ansi = use_ansi
        self.show_path: bool = False
        self.color_index: int = 0

    def render(self) -> str:
        """Render the current maze state into a displayable string."""
        grid = self.generator.get_grid()
        path: Optional[List[Tuple[int, int]]] = None
        if self.show_path:
            path = self.generator.get_solution_path()

        return render_ascii_grid(
            grid=grid,
            entry=self.generator.entry,
            exit_coord=self.generator.exit,
            path=path,
            color_index=self.color_index,
            use_ansi=self.use_ansi,
        )

    def toggle_path(self) -> bool:
        """Toggle solution path visibility.

        Returns:
            New state of show_path.
        """
        self.show_path = not self.show_path
        return self.show_path

    def rotate_color(self) -> str:
        """Rotate wall color to the next palette entry.

        Returns:
            Name of new active wall color.
        """
        self.color_index = (self.color_index + 1) % len(WALL_PALETTE)
        return WALL_PALETTE[self.color_index][1]

    def regenerate(self) -> None:
        """Generate a fresh maze with a new random seed."""
        if self.generator.seed is not None:
            self.generator.seed += 1
        self.generator.generate()

    def run_menu_loop(
        self,
        input_fn: Callable[[str], str] = input,
        print_fn: Callable[[str], None] = print,
    ) -> None:
        """Run the interactive visualizer CLI loop.

        Args:
            input_fn: Function to gather user input (default: builtin input).
            print_fn: Function to display output (default: builtin print).
        """
        while True:
            # Display maze
            print_fn(self.render())
            # Display menu matching subject page 14
            print_fn("=== A-Maze-ing ===")
            print_fn("1. Re-generate a new maze")
            status = "ON" if self.show_path else "OFF"
            print_fn(f"2. Show/Hide path from entry to exit (Currently: {status})")
            _, color_name = WALL_PALETTE[self.color_index % len(WALL_PALETTE)]
            print_fn(f"3. Rotate maze colors (Currently: {color_name})")
            print_fn("4. Quit")

            try:
                choice = input_fn("Choice? (1-4): ").strip()
            except (EOFError, KeyboardInterrupt):
                print_fn("\nExiting visualizer.")
                break

            if choice == "1":
                self.regenerate()
            elif choice == "2":
                self.toggle_path()
            elif choice == "3":
                self.rotate_color()
            elif choice == "4":
                print_fn("Goodbye!")
                break
            else:
                print_fn(f"Invalid option: '{choice}'. Please enter 1, 2, 3, or 4.\n")
