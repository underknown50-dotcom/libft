import sys
import typing


def print_usage() -> None:
    print("Usage: ft_ancient_text.py <file>")


def get_filename() -> str | None:
    if len(sys.argv) != 2:
        print_usage()
        return None
    return sys.argv[1]


def display_header(filename: str) -> None:
    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file '{filename}'")


def read_file_lines(filename: str) -> list[str] | None:
    lines: list[str] = []
    file: typing.IO[str] | None = None

    try:
        file = open(filename, "r")

        for line in file:
            lines.append(line)

        return lines

    except OSError as error:
        print(f"Error opening file '{filename}': {error}")
        return None

    finally:
        if file is not None:
            file.close()


def display_content(lines: list[str]) -> None:
    print("---")

    for line in lines:
        print(line, end="")

    print("---")


def display_closed_message(filename: str) -> None:
    print(f"File '{filename}' closed.")


def main() -> None:
    filename = get_filename()

    if filename is None:
        return

    display_header(filename)

    lines = read_file_lines(filename)

    if lines is None:
        return

    display_content(lines)
    display_closed_message(filename)


if __name__ == "__main__":
    main()
