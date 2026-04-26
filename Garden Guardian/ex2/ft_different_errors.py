def garden_operations(operation_number: int) -> None:
    if operation_number == 0:
        int("abc")
    elif operation_number == 1:
        1 / 0
    elif operation_number == 2:
        open("/non/existent/file")
    elif operation_number == 3:
        "Hello" + 1
    else:
        return


def test_error_types() -> None:
    operations = [0, 1, 2, 3, 4]

    print("=== Garden Error Types Demo ===")

    for op in operations:
        print(f"Testing operation {op}...")
        try:
            garden_operations(op)
            print("Operation completed successfully")
        except ValueError as error:
            print(f"Caught ValueError: {error}")
        except ZeroDivisionError as error:
            print(f"Caught ZeroDivisionError: {error}")
        except FileNotFoundError as error:
            print(f"Caught FileNotFoundError: {error}")
        except TypeError as error:
            print(f"Caught TypeError: {error}")

    # ✅ Required part: multiple exceptions in ONE except
    print("\nTesting multiple exception catch...")
    try:
        garden_operations(0)  # any failing case
    except (ValueError, ZeroDivisionError, FileNotFoundError, TypeError) as error:
        print(f"Caught multiple error types: {error}")

    print("All error types tested successfully!")


if __name__ == "__main__":
    test_error_types()
