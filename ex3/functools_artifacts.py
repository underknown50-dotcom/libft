from collections.abc import Callable
from functools import reduce, partial, lru_cache, singledispatch
from operator import add, mul
from typing import Any


def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return 0

    if operation == "add":
        return reduce(add, spells)
    elif operation == "multiply":
        return reduce(mul, spells)
    elif operation == "max":
        return max(spells)
    elif operation == "min":
        return min(spells)
    else:
        raise ValueError(f"Unknown operation: {operation}")


def partial_enchanter(
    base_enchantment: Callable[[int, str, str], str],
) -> dict[str, Callable[[str], str]]:
    elements: list[str] = ["fire", "ice", "lightning"]
    return {
        elem: partial(base_enchantment, 50, elem)
        for elem in elements
    }


@lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n < 2:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:
    @singledispatch
    def dispatch(arg: Any) -> str:
        return "Unknown spell type"

    @dispatch.register(int)
    def _(arg: int) -> str:
        return f"Damage spell: {arg} damage"

    @dispatch.register(str)
    def _(arg: str) -> str:
        return f"Enchantment: {arg}"

    @dispatch.register(list)
    def _(arg: list[Any]) -> str:
        return f"Multi-cast: {len(arg)} spells"

    return dispatch


if __name__ == "__main__":
    print("Testing spell reducer...")
    spells: list[int] = [10, 20, 30, 40]
    print(f"Sum: {spell_reducer(spells, 'add')}")
    print(f"Product: {spell_reducer(spells, 'multiply')}")
    print(f"Max: {spell_reducer(spells, 'max')}")
    print(f"Min: {spell_reducer(spells, 'min')}")

    print("\nTesting memoized fibonacci...")
    print(f"Fib(0): {memoized_fibonacci(0)}")
    print(f"Fib(1): {memoized_fibonacci(1)}")
    print(f"Fib(10): {memoized_fibonacci(10)}")
    print(f"Fib(15): {memoized_fibonacci(15)}")
    print(f"Cache info: {memoized_fibonacci.cache_info()}")

    print("\nTesting spell dispatcher...")
    dispatcher = spell_dispatcher()
    print(dispatcher(42))
    print(dispatcher("fireball"))
    print(dispatcher([1, 2, 3]))
    print(dispatcher(3.14))

    print("\nTesting partial enchanter...")

    def base_enchant(power: int, element: str, target: str) -> str:
        return f"{element.upper()} {target} with power {power}"

    enchanters = partial_enchanter(base_enchant)
    fire = enchanters["fire"]
    ice = enchanters["ice"]
    lightning = enchanters["lightning"]
    print(fire("Dragon"))
    print(ice("Golem"))
    print(lightning("Troll"))
