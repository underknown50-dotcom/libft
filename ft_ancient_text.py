import sys
from typing import NoReturn, Optional, TextIO


def print_usage() -> NoReturn:
    print("Usage: ft_ancient_text.py <file>")
    sys.exit(1)


def get_filename() -> str:
    if len(sys.argv) != 2:
        print_usage()
    return sys.argv[1]


def display_header(filename: str) -> None:
    print("== Cyber Archives Recovery ==")
    print(f"Accessing file '{filename}'")


def read_and_display_file(filename: str) -> None:
    f = None
    try:
        f = open(filename, 'r')
        for line in f:
            print(line, end='')
    except OSError as e:
        print(f"Error opening file '{filename}': {e}")
        sys.exit(1)
    finally:
        if f is not None:
            f.close()
            print(f"File '{filename}' closed.")


def main() -> None:
    filename = get_filename()
    display_header(filename)
    read_and_display_file(filename)


if __name__ == "__main__":
    main()
