import sys
from typing import Optional, TextIO, List


def print_usage() -> None:
    print("Usage: ft_archive_creation.py <file>")


def get_filename() -> Optional[str]:
    if len(sys.argv) != 2:
        print_usage()
        return None
    return sys.argv[1]


def display_header(filename: str) -> None:
    print("== Cyber Archives Recovery & Preservation ==")
    print(f"Accessing file '{filename}'\n")


def read_file_lines(filename: str) -> Optional[List[str]]:
    lines: List[str] = []
    f: Optional[TextIO] = None
    try:
        f = open(filename, 'r')
        for line in f:
            lines.append(line)
        return lines
    except OSError as e:
        print(f"Error opening file '{filename}': {e}")
        return None
    finally:
        if f is not None:
            f.close()


def display_content(lines: List[str]) -> None:
    for line in lines:
        print(line, end='')
    print()


def display_closed_message(filename: str) -> None:
    print(f"File '{filename}' closed.\n")


def transform_lines(lines: List[str]) -> List[str]:
    transformed: List[str] = []
    for line in lines:
        transformed.append(line.rstrip('\n') + '#\n')
    return transformed


def display_transformed_content(lines: List[str]) -> None:
    print("Transform data:\n")
    for line in lines:
        print(line, end='')
    print()


def ask_output_filename() -> Optional[str]:
    name = input("Enter new file name (or empty): ").strip()
    return name if name else None


def save_lines_to_file(filename: str, lines: List[str]) -> bool:
    f: Optional[TextIO] = None
    try:
        f = open(filename, 'w')
        f.writelines(lines)
        print(f"Saving data to '{filename}'")
        print(f"Data saved in file '{filename}'.")
        return True
    except OSError as e:
        print(f"Error writing to file '{filename}': {e}")
        return False
    finally:
        if f is not None:
            f.close()


def main() -> int:
    filename = get_filename()
    if filename is None:
        return 1

    display_header(filename)

    original_lines = read_file_lines(filename)
    if original_lines is None:
        return 1

    display_content(original_lines)
    display_closed_message(filename)

    transformed_lines = transform_lines(original_lines)

    display_transformed_content(transformed_lines)

    output_filename = ask_output_filename()
    if output_filename is None:
        print("Not saving data.")
        return 0

    success = save_lines_to_file(output_filename, transformed_lines)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
