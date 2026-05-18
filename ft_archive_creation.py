#!/usr/bin/env python3

import sys
from typing import NoReturn, Optional, TextIO, List


def print_usage() -> NoReturn:
    print("Usage: ft_archive_creation.py <file>")
    sys.exit(1)


def get_filename() -> str:
    if len(sys.argv) != 2:
        print_usage()
    return sys.argv[1]


def display_header(filename: str) -> None:
    print("== Cyber Archives Recovery & Preservation ==")
    print(f"Accessing file '{filename}'\n")


def read_and_display_file(filename: str) -> List[str]:
    lines: List[str] = []
    f: Optional[TextIO] = None
    try:
        f = open(filename, 'r')
        for line in f:
            print(line, end='')
            lines.append(line)
    except OSError as e:
        print(f"Error opening file '{filename}': {e}")
        sys.exit(1)
    finally:
        if f is not None:
            f.close()
            print(f"File '{filename}' closed.\n")
    return lines


def transform_and_display(lines: List[str]) -> List[str]:
    transformed: List[str] = []
    print("Transform data:\n")
    for line in lines:
        new_line = line.rstrip('\n') + '#\n'
        print(new_line, end='')
        transformed.append(new_line)
    print()
    return transformed


def ask_and_save(transformed: List[str]) -> None:
    new_filename = input("Enter new file name (or empty): ").strip()
    if not new_filename:
        print("Not saving data.")
        return

    f_out: Optional[TextIO] = None
    try:
        f_out = open(new_filename, 'w')
        f_out.writelines(transformed)
        print(f"Saving data to '{new_filename}'")
        print(f"Data saved in file '{new_filename}'.")
    except OSError as e:
        print(f"Error writing to file '{new_filename}': {e}")
        sys.exit(1)
    finally:
        if f_out is not None:
            f_out.close()


def main() -> None:
    filename = get_filename()
    display_header(filename)
    original_lines = read_and_display_file(filename)
    transformed_lines = transform_and_display(original_lines)
    ask_and_save(transformed_lines)


if __name__ == "__main__":
    main()
