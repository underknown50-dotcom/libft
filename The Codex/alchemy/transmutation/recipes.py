from ..elements import create_air
from alchemy.potions import strength_potion
from elements import create_fire


def lead_to_gold() -> str:
    return (
        "Recipe transmuting Lead to Gold: brew '{}' and '{}' "
        "mixed with '{}'".format(
            create_air(), strength_potion(), create_fire()
        )
    )
