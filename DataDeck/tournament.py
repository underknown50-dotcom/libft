from typing import List, Tuple
from ex0 import FlameFactory, AquaFactory, CreatureFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import (
    NormalStrategy,
    AggressiveStrategy,
    DefensiveStrategy,
    BattleStrategy,
)


def run_tournament(
    opponents: List[Tuple[CreatureFactory, BattleStrategy]]
) -> None:
    print(f"{len(opponents)} opponents involved")
    creatures = [
        (factory.create_base(), strategy)
        for factory, strategy in opponents
    ]
    n = len(creatures)

    for i in range(n):
        for j in range(i + 1, n):
            creature1, strategy1 = creatures[i]
            creature2, strategy2 = creatures[j]

            print("* Battle *")
            print(creature1.describe())
            print("vs.")
            print(creature2.describe())
            print("now fight!")

            try:
                strategy1.act(creature1)
                strategy2.act(creature2)
            except ValueError as e:
                print(f"Battle error, aborting tournament: {e}")
                return

            print()


def main() -> None:
    print("Tournament 0 (basic)")
    print("[ (Flameling+Normal), (Healing+Defensive) ]")
    print("*** Tournament ***")
    opponents0 = [
        (FlameFactory(), NormalStrategy()),
        (HealingCreatureFactory(), DefensiveStrategy()),
    ]
    run_tournament(opponents0)
    print()

    print("Tournament 1 (error)")
    print("[ (Flameling+Aggressive), (Healing+Defensive) ]")
    print("*** Tournament ***")
    opponents1 = [
        (FlameFactory(), AggressiveStrategy()),
        (HealingCreatureFactory(), DefensiveStrategy()),
    ]
    run_tournament(opponents1)
    print()

    print("Tournament 2 (multiple)")
    print("[ (Aquabub+Normal), (Healing+Defensive), (Transform+Aggressive) ]")
    print("*** Tournament ***")
    opponents2 = [
        (AquaFactory(), NormalStrategy()),
        (HealingCreatureFactory(), DefensiveStrategy()),
        (TransformCreatureFactory(), AggressiveStrategy()),
    ]
    run_tournament(opponents2)


if __name__ == "__main__":
    main()
