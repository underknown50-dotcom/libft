def garden_operations(operation_number: int) -> None:
    if operation_number == 0:
        int("abc")
    elif operation_number == 1:
        1 / 0
    elif operation_number == 2:
        open("/non/existent/file")
    elif operation_number == 3:
        "Hello" + 1


def display_header() -> None:
    print("=== Garden Error Types Demo ===")


def display_operation(operation_number: int) -> None:
    print(f"Testing operation {operation_number}...")


def display_success() -> None:
    print("Operation completed successfully")


def display_grouped_error(error: FileNotFoundError | TypeError) -> None:
    print(f"Caught {error.__class__.__name__}: {error}")


def handle_operation(operation_number: int) -> None:
    display_operation(operation_number)

    try:
        garden_operations(operation_number)
        display_success()
    except ValueError as error:
        print(f"Caught ValueError: {error}")
    except ZeroDivisionError as error:
        print(f"Caught ZeroDivisionError: {error}")
    except (FileNotFoundError, TypeError) as error:
        display_grouped_error(error)


def test_error_types() -> None:
    display_header()

    for operation_number in range(5):
        handle_operation(operation_number)

    print("\nAll error types tested successfully!")


if __name__ == "__main__":
    test_error_types()
