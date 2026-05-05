import sys


def print_header() -> None:
    print("=== Inventory System Analysis ===")


def parse_inventory_argument(argument: str, inventory: dict[str, int]) -> None:
    parts = argument.split(":")

    if len(parts) != 2:
        print(f"Error - invalid parameter '{argument}'")
        return

    item_name = parts[0]
    quantity_text = parts[1]

    if item_name in inventory:
        print(f"Redundant item '{item_name}' - discarding")
        return

    try:
        quantity = int(quantity_text)
    except ValueError as error:
        print(f"Quantity error for '{item_name}': {error}")
        return

    inventory[item_name] = quantity


def create_inventory(arguments: list[str]) -> dict[str, int]:
    inventory: dict[str, int] = {}
    index = 1

    while index < len(arguments):
        parse_inventory_argument(arguments[index], inventory)
        index += 1

    return inventory


def print_inventory(inventory: dict[str, int]) -> None:
    print("Got inventory:", inventory)


def print_item_list(inventory: dict[str, int]) -> None:
    item_list = list(inventory.keys())
    print("Item list:", item_list)


def get_total_quantity(inventory: dict[str, int]) -> int:
    return sum(inventory.values())


def print_total_quantity(
    inventory: dict[str, int],
    total_quantity: int,
) -> None:
    print(
        f"Total quantity of the {len(inventory)} items: "
        f"{total_quantity}"
    )


def print_quantity_percentages(
    inventory: dict[str, int],
    total_quantity: int,
) -> None:
    if total_quantity == 0:
        return

    for item in inventory:
        percentage = inventory[item] / total_quantity * 100
        print(f"Item {item} represents {round(percentage, 1)}%")


def print_most_abundant_item(inventory: dict[str, int]) -> None:
    if not inventory:
        return

    most_item: str | None = None
    most_quantity = -1

    for item in inventory:
        if inventory[item] > most_quantity:
            most_item = item
            most_quantity = inventory[item]

    if most_item is not None:
        print(
            f"Item most abundant: {most_item} "
            f"with quantity {most_quantity}"
        )


def print_least_abundant_item(inventory: dict[str, int]) -> None:
    if not inventory:
        return

    items = list(inventory.keys())
    least_item = items[0]
    least_quantity = inventory[least_item]

    for item in inventory:
        if inventory[item] < least_quantity:
            least_item = item
            least_quantity = inventory[item]

    print(
        f"Item least abundant: {least_item} "
        f"with quantity {least_quantity}"
    )


def add_magic_item(inventory: dict[str, int]) -> None:
    inventory["magic_item"] = 1


def print_updated_inventory(inventory: dict[str, int]) -> None:
    print("Updated inventory:", inventory)


def main() -> None:
    print_header()

    inventory = create_inventory(sys.argv)

    if not inventory:
        print_inventory(inventory)
        return

    print_inventory(inventory)
    print_item_list(inventory)

    total_quantity = get_total_quantity(inventory)
    print_total_quantity(inventory, total_quantity)

    print_quantity_percentages(inventory, total_quantity)

    print_most_abundant_item(inventory)
    print_least_abundant_item(inventory)

    add_magic_item(inventory)
    print_updated_inventory(inventory)


if __name__ == "__main__":
    main()
