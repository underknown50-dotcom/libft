import sys
from typing import Optional, TextIO, List


def print_usage() -> None:
    sys.stdout.write("Usage: ft_stream_management.py <file>\n")


def get_filename() -> Optional[str]:
    if len(sys.argv) != 2:
        print_usage()
        return None
    return sys.argv[1]


def display_header(filename: str) -> None:
    sys.stdout.write(f"Accessing file '{filename}'\n\n")


def read_file_lines(filename: str) -> Optional[List[str]]:
    lines: List[str] = []
    f: Optional[TextIO] = None
    try:
        f = open(filename, 'r')
        for line in f:
            lines.append(line)
        return lines
    except OSError as e:
        sys.stderr.write(f"[STDERR] Error opening file '{filename}': {e}\n")
        return None
    finally:
        if f is not None:
            f.close()


def display_content(lines: List[str]) -> None:
    for line in lines:
        sys.stdout.write(line)
    sys.stdout.write("\n")


def display_closed_message(filename: str) -> None:
    sys.stdout.write(f"File '{filename}' closed.\n\n")


def transform_lines(lines: List[str]) -> List[str]:
    transformed: List[str] = []
    for line in lines:
        transformed.append(line.rstrip('\n') + '#\n')
    return transformed


def display_transformed_content(lines: List[str]) -> None:
    sys.stdout.write("Transform data:\n\n")
    for line in lines:
        sys.stdout.write(line)
    sys.stdout.write("\n")


def ask_output_filename() -> Optional[str]:
    sys.stdout.write("Enter new file name (or empty): ")
    sys.stdout.flush()
    name = sys.stdin.readline().rstrip('\n')
    return name if name else None


def save_lines_to_file(filename: str, lines: List[str]) -> bool:
    f: Optional[TextIO] = None
    try:
        f = open(filename, 'w')
        f.writelines(lines)
        sys.stdout.write(f"Saving data to '{filename}'\n")
        sys.stdout.write(f"Data saved in file '{filename}'.\n")
        return True
    except OSError as e:
        sys.stderr.write(f"[STDERR] Error opening file '{filename}': {e}\n")
        sys.stdout.write("Data not saved.\n")
        return False
    finally:
        if f is not None:
            f.close()


def main() -> int:
    filename = get_filename()
    if filename is None:
        return 1

    # Header
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
        sys.stdout.write("Not saving data.\n")
        return 0

    success = save_lines_to_file(output_filename, transformed_lines)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
