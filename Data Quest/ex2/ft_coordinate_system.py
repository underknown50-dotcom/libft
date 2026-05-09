import math


def print_header() -> None:
    print("=== Game Coordinate System ===")


def parse_coordinates(user_input: str) -> tuple[float, float, float] | None:
    parts = user_input.split(",")

    if len(parts) != 3:
        print("Invalid syntax")
        return None

    try:
        x = float(parts[0])
    except ValueError as error:
        print(f"Error on parameter '{parts[0]}': {error}")
        return None

    try:
        y = float(parts[1])
    except ValueError as error:
        print(f"Error on parameter '{parts[1]}': {error}")
        return None

    try:
        z = float(parts[2])
    except ValueError as error:
        print(f"Error on parameter '{parts[2]}': {error}")
        return None

    return (x, y, z)


def get_player_pos() -> tuple[float, float, float]:
    while True:
        user_input = input(
            "Enter new coordinates as floats in format 'x,y,z': "
        )

        position = parse_coordinates(user_input)

        if position is not None:
            return position


def distance_between_points(
    first_position: tuple[float, float, float],
    second_position: tuple[float, float, float],
) -> float:
    x_distance = second_position[0] - first_position[0]
    y_distance = second_position[1] - first_position[1]
    z_distance = second_position[2] - first_position[2]

    return math.sqrt(
        (x_distance ** 2)
        + (y_distance ** 2)
        + (z_distance ** 2)
    )


def distance_from_center(position: tuple[float, float, float]) -> float:
    return distance_between_points(position, (0.0, 0.0, 0.0))


def print_position_details(position: tuple[float, float, float]) -> None:
    print(f"Got a first tuple: {position}")
    print(
        f"It includes: X={position[0]}, "
        f"Y={position[1]}, "
        f"Z={position[2]}"
    )


def main() -> None:
    print_header()

    print("Get a first set of coordinates")
    first_position = get_player_pos()

    print_position_details(first_position)

    center_distance = distance_from_center(first_position)
    print(f"Distance to center: {center_distance:.4f}")

    print("\nGet a second set of coordinates")
    second_position = get_player_pos()

    points_distance = distance_between_points(
        first_position,
        second_position,
    )
    print(f"Distance between the 2 sets of coordinates: {points_distance:.4f}")


if __name__ == "__main__":
    main()
