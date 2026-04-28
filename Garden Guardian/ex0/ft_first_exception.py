def input_temperature(temp_str: str) -> int:
    return int(temp_str)


def display_header() -> None:
    print("=== Garden Temperature ===\n")


def display_input(data: str) -> None:
    print(f"Input data is '{data}'")


def display_temperature(temp: int) -> None:
    print(f"Temperature is now {temp}°C\n")


def display_error(error: ValueError) -> None:
    print(f"Caught input_temperature error: {error}\n")


def test_one_temperature(data: str) -> None:
    display_input(data)

    try:
        temp = input_temperature(data)
        display_temperature(temp)
    except ValueError as error:
        display_error(error)


def test_temperature() -> None:
    display_header()

    test_cases = ["25", "abc"]

    for data in test_cases:
        test_one_temperature(data)

    print("All tests completed - program didn't crash!")


if __name__ == "__main__":
    test_temperature()
