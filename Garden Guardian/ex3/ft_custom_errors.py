class GardenError(Exception):
    def __init__(self, message: str = "Unknown garden error") -> None:
        super().__init__(message)


class PlantError(GardenError):
    def __init__(self, message: str = "Unknown plant error") -> None:
        super().__init__(message)


class WaterError(GardenError):
    def __init__(self, message: str = "Unknown watering error") -> None:
        super().__init__(message)


def raise_plant_error() -> None:
    raise PlantError("The tomato plant is wilting!")


def raise_water_error() -> None:
    raise WaterError("Not enough water in the tank!")


def display_header() -> None:
    print("=== Custom Garden Errors Demo ===\n")


def test_plant_error() -> None:
    print("Testing PlantError...")

    try:
        raise_plant_error()
    except PlantError as error:
        print(f"Caught PlantError: {error}")


def test_water_error() -> None:
    print("Testing WaterError...")

    try:
        raise_water_error()
    except WaterError as error:
        print(f"Caught WaterError: {error}")


def test_all_garden_errors() -> None:
    print("\nTesting catching all garden errors...")

    for function in (raise_plant_error, raise_water_error):
        try:
            function()
        except GardenError as error:
            print(f"Caught GardenError: {error}")


def test_custom_errors() -> None:
    display_header()
    test_plant_error()
    test_water_error()
    test_all_garden_errors()
    print("\nAll custom error types work correctly!")


if __name__ == "__main__":
    test_custom_errors()
