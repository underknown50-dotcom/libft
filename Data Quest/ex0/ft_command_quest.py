import sys


def print_header() -> None:
    print("=== Command Quest ===")


def print_program_name(program_name: str) -> None:
    print(f"Program name: {program_name}")


def has_arguments(arguments: list[str]) -> bool:
    return len(arguments) > 1


def print_no_arguments() -> None:
    print("No arguments provided!")


def print_arguments_count(arguments: list[str]) -> None:
    print(f"Arguments received: {len(arguments) - 1}")


def print_arguments(arguments: list[str]) -> None:
    index = 1
    while index < len(arguments):
        print(f"Argument {index}: {arguments[index]}")
        index += 1


def print_total_arguments(arguments: list[str]) -> None:
    print(f"Total arguments: {len(arguments)}")


def main() -> None:
    arguments = sys.argv

    print_header()
    print_program_name(arguments[0])
    if has_arguments(arguments):
        print_arguments_count(arguments)
        print_arguments(arguments)
    else:
        print_no_arguments()

    print_total_arguments(arguments)


if __name__ == "__main__":
    main()
