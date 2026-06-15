from ex0 import CreatureFactory, FlameFactory, AquaFactory


def test_factory(factory: CreatureFactory) -> None:
    base = factory.create_base()
    evolved = factory.create_evolved()
    print(base.describe())
    print(base.attack())
    print(evolved.describe())
    print(evolved.attack())


def fight(factory1: CreatureFactory, factory2: CreatureFactory) -> None:
    c1 = factory1.create_base()
    c2 = factory2.create_base()
    print(c1.describe())
    print("vs.")
    print(c2.describe())
    print("fight!")
    print(c1.attack())
    print(c2.attack())


def main() -> None:
    flame_factory = FlameFactory()
    aqua_factory = AquaFactory()

    print("Testing factory")
    test_factory(flame_factory)
    print()

    print("Testing factory")
    test_factory(aqua_factory)
    print()

    print("Testing battle")
    fight(flame_factory, aqua_factory)


if __name__ == "__main__":
    main()
