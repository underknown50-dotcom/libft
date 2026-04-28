def input_temperature(temp_str: str) -> int:
    temp = int(temp_str)
    validate_temperature(temp)
    return temp


def validate_temperature(temp: int) -> None:
    if temp < 0:
        raise ValueError(f"{temp}°C is too cold for plants (min 0°C)")
    if temp > 40:
        raise ValueError(f"{temp}°C is too hot for plants (max 40°C)")


def display_header() -> None:
    print("=== Garden Temperature Checker ===\n")


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

    test_cases = ["25", "abc", "100", "-50"]

    for data in test_cases:
        test_one_temperature(data)

    print("All tests completed - program didn't crash!")


if __name__ == "__main__":
    test_temperature()
