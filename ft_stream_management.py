import sys
from typing import NoReturn, Optional, TextIO, List


def print_usage() -> NoReturn:
    sys.stdout.write("Usage: ft_stream_management.py <file>\n")
    sys.exit(1)


def get_filename() -> str:
    if len(sys.argv) != 2:
        print_usage()
    return sys.argv[1]


def display_header(filename: str) -> None:
    sys.stdout.write("== Cyber Archives Recovery & Preservation ==\n")
    sys.stdout.write(f"Accessing file '{filename}'\n\n")


def read_and_display_file(filename: str) -> List[str]:
    lines: List[str] = []
    f: Optional[TextIO] = None
    try:
        f = open(filename, 'r')
        for line in f:
            sys.stdout.write(line)
            lines.append(line)
    except OSError as e:
        sys.stderr.write(f"[STDERR] Error opening file '{filename}': {e}\n")
        sys.exit(1)
    finally:
        if f is not None:
            f.close()
            sys.stdout.write(f"File '{filename}' closed.\n\n")
    return lines


def transform_and_display(lines: List[str]) -> List[str]:
    transformed: List[str] = []
    sys.stdout.write("Transform data:\n\n")
    for line in lines:
        new_line = line.rstrip('\n') + '#\n'
        sys.stdout.write(new_line)
        transformed.append(new_line)
    sys.stdout.write("\n")
    return transformed


def ask_and_save(transformed: List[str]) -> None:
    sys.stdout.write("Enter new file name (or empty): ")
    sys.stdout.flush()
    new_filename = sys.stdin.readline().rstrip('\n')
    if not new_filename:
        sys.stdout.write("Not saving data.\n")
        return

    f_out: Optional[TextIO] = None
    try:
        f_out = open(new_filename, 'w')
        f_out.writelines(transformed)
        sys.stdout.write(f"Saving data to '{new_filename}'\n")
        sys.stdout.write(f"Data saved in file '{new_filename}'.\n")
    except OSError as e:
        sys.stderr.write(
            f"[STDERR] Error opening file '{new_filename}': {e}\n"
        )
        sys.stdout.write("Data not saved.\n")
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
