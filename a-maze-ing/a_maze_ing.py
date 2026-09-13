"""A-Maze-ing: Maze generator main entry point."""

import sys


def main() -> int:
    """Run the main entry point of the maze generator application.

    Returns:
        int: Exit status code (0 for success, non-zero for failure).
    """
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: python3 a_maze_ing.py config.txt\n")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
