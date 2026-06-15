from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex1.capabilities import HealCapability, TransformCapability


def main() -> None:
    healing_factory = HealingCreatureFactory()
    print("Testing Creature with healing capability")

    base = healing_factory.create_base()
    print("base:")
    print(base.describe())
    print(base.attack())
    assert isinstance(base, HealCapability)
    print(base.heal())

    evolved = healing_factory.create_evolved()
    print("evolved:")
    print(evolved.describe())
    print(evolved.attack())
    assert isinstance(evolved, HealCapability)
    print(evolved.heal())

    print()

    transform_factory = TransformCreatureFactory()
    print("Testing Creature with transform capability")

    base = transform_factory.create_base()
    print("base:")
    print(base.describe())
    print(base.attack())
    assert isinstance(base, TransformCapability)
    print(base.transform())
    print(base.attack())
    print(base.revert())

    evolved = transform_factory.create_evolved()
    print("evolved:")
    print(evolved.describe())
    print(evolved.attack())
    assert isinstance(evolved, TransformCapability)
    print(evolved.transform())
    print(evolved.attack())
    print(evolved.revert())


if __name__ == "__main__":
    main()
