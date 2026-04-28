class GardenError(Exception):
    def __init__(self, message: str = "Unknown garden error") -> None:
        super().__init__(message)


class PlantError(GardenError):
    def __init__(self, message: str = "Unknown plant error") -> None:
        super().__init__(message)


def display_header() -> None:
    print("=== Garden Watering System ===")


def open_watering_system() -> None:
    print("Opening watering system")


def close_watering_system() -> None:
    print("Closing watering system\n")


def water_plant(plant_name: str) -> None:
    if not plant_name or not plant_name[0].isupper():
        raise PlantError(f"Invalid plant name to water: '{plant_name}'")

    print(f"Watering {plant_name}: [OK]")


def water_plants(plant_names: list[str]) -> None:
    try:
        open_watering_system()

        for plant_name in plant_names:
            water_plant(plant_name)

    except PlantError as error:
        print(f"Caught PlantError: {error}")
        print("... ending tests and returning to main")
        return

    finally:
        close_watering_system()


def test_watering_system() -> None:
    display_header()

    print("Testing valid plants...")
    water_plants(["Tomato", "Lettuce", "Carrots"])

    print("Testing invalid plants...")
    water_plants(["Tomato", "lettuce"])

    print("\nCleanup always happens, even with errors!")


if __name__ == "__main__":
    test_watering_system()
