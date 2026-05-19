#!/usr/bin/env python3

import sys
from typing import Optional, TextIO, List


def print_usage() -> None:
    print("Usage: ft_ancient_text.py <file>")


def get_filename() -> Optional[str]:
    if len(sys.argv) != 2:
        print_usage()
        return None
    return sys.argv[1]


def display_header(filename: str) -> None:
    print("== Cyber Archives Recovery ==")
    print(f"Accessing file '{filename}'")


def read_file_lines(filename: str) -> Optional[List[str]]:
    """Return list of lines (with newlines) on success, None on error."""
    lines: List[str] = []
    f: Optional[TextIO] = None
    try:
        f = open(filename, 'r')
        for line in f:
            lines.append(line)
        return lines
    except (OSError, UnicodeDecodeError) as e:
        print(f"Error opening file '{filename}': {e}")
        return None
    finally:
        if f is not None:
            f.close()
            print(f"File '{filename}' closed.")


def display_content(lines: List[str]) -> None:
    """Print each line as-is (preserving original newlines)."""
    for line in lines:
        print(line, end='')


def main() -> int:
    filename = get_filename()
    if filename is None:
        return 1

    display_header(filename)
    lines = read_file_lines(filename)
    if lines is None:
        return 1

    display_content(lines)
    return 0


if __name__ == "__main__":
    sys.exit(main())
