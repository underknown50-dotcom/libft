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
