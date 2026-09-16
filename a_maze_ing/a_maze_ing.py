#!/usr/bin/env python3
"""Main program entrypoint for A-Maze-ing conforming to Chapter 4 & 5."""

import sys
from pathlib import Path
from typing import List

# Ensure UTF-8 output encoding for cross-platform terminal rendering
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure src/ is on sys.path when running standalone without prior pip install
_src_dir = str(Path(__file__).resolve().parent / "src")
if _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)

from mazegen import (  # noqa: E402
    ConfigError,
    ConfigFileNotFoundError,
    ConfigSyntaxError,
    ConfigValueError,
    InteractiveVisualizer,
    MazeGenerator,
    NoPathFoundError,
    export_maze,
    parse_config,
)


def main(argv: List[str]) -> int:
    """Execute main application workflow.

    Args:
        argv: Command-line arguments.

    Returns:
        Exit code: 0 on success, non-zero on error.
    """
    if len(argv) != 2:
        print(
            "Error: Invalid arguments.\n"
            "Usage: python3 a_maze_ing.py <config_file>",
            file=sys.stderr,
        )
        return 1

    config_path = argv[1]

    try:
        # 1. Parse configuration
        config = parse_config(config_path)

        # 2. Generate maze
        generator = MazeGenerator.from_config(config)
        grid = generator.generate()

        # 3. Solve maze
        _, solution_str = generator.solve()

        # 4. Export output file adhering to Chapter 4.5
        export_maze(
            config.output_file,
            grid,
            config.entry,
            config.exit,
            solution_str,
        )
        print(f"Maze successfully written to '{config.output_file}'.")

        # 5. Visual representation and interaction (Chapter 5)
        visualizer = InteractiveVisualizer(generator)
        if sys.stdin.isatty():
            visualizer.run_menu_loop()
        else:
            # Non-interactive mode (e.g. automated test / redirected input)
            print(visualizer.render())

        return 0

    except ConfigFileNotFoundError as err:
        print(f"Configuration File Error: {err}", file=sys.stderr)
        return 1
    except ConfigSyntaxError as err:
        print(f"Configuration Syntax Error: {err}", file=sys.stderr)
        return 1
    except ConfigValueError as err:
        print(f"Configuration Value Error: {err}", file=sys.stderr)
        return 1
    except ConfigError as err:
        print(f"Configuration Error: {err}", file=sys.stderr)
        return 1
    except NoPathFoundError as err:
        print(f"Pathfinding Error: {err}", file=sys.stderr)
        return 1
    except OSError as err:
        print(f"File System Error: {err}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        return 0
    except Exception as err:
        print(f"Unexpected Error: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
