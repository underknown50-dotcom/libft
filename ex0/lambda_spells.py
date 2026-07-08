from typing import TypedDict


class Artifact(TypedDict):
    name: str
    power: int
    type: str


class Mage(TypedDict):
    name: str
    power: int
    element: str


def artifact_sorter(artifacts: list[Artifact]) -> list[Artifact]:
    return sorted(artifacts, key=lambda x: x['power'], reverse=True)


def power_filter(mages: list[Mage], min_power: int) -> list[Mage]:
    return list(filter(lambda x: x['power'] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda x: "* " + x + " *", spells))


def mage_stats(mages: list[Mage]) -> dict[str, int | float | None]:
    if not mages:
        return {'max_power': None, 'min_power': None, 'avg_power': None}
    return {
        'max_power': max(mages, key=lambda m: m['power'])['power'],
        'min_power': min(mages, key=lambda m: m['power'])['power'],
        'avg_power': round(sum(m['power'] for m in mages) / len(mages), 2)
    }


if __name__ == "__main__":
    artifacts: list[Artifact] = [
        {"name": "Fire Staff", "power": 92, "type": "weapon"},
        {"name": "Crystal Orb", "power": 85, "type": "focus"},
        {"name": "Shadow Amulet", "power": 78, "type": "amulet"},
    ]

    mages: list[Mage] = [
        {"name": "Alex", "power": 30, "element": "fire"},
        {"name": "Jordan", "power": 50, "element": "water"},
        {"name": "Riley", "power": 20, "element": "earth"},
    ]

    spells: list[str] = ["fireball", "heal", "shield"]

    print("Testing artifact sorter...")
    sorted_artifacts = artifact_sorter(artifacts)
    for a in sorted_artifacts:
        print(f"{a['name']} ({a['power']} power)")
    print()

    print("Testing power filter (min_power=25)...")
    filtered = power_filter(mages, 25)
    for m in filtered:
        print(f"{m['name']} - {m['power']} power")
    print()

    print("Testing spell transformer...")
    transformed = spell_transformer(spells)
    print(" ".join(transformed))
    print()

    print("Testing mage stats...")
    stats = mage_stats(mages)
    print(f"Max power: {stats['max_power']}")
    print(f"Min power: {stats['min_power']}")
    print(f"Average power: {stats['avg_power']}")
