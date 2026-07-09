from collections.abc import Callable
from functools import wraps
import time
import inspect
from typing import Any


def spell_timer(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Casting {func.__name__}...")
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"Spell completed in {elapsed:.3f} seconds")
        return result
    return wrapper


def power_validator(
    min_power: int,
) -> Callable[
    [Callable[..., Any]],
    Callable[..., Any],
]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            power = bound.arguments.get('power')

            if power is None:
                raise ValueError("Function must have a 'power' parameter")

            if power >= min_power:
                return func(*args, **kwargs)
            return "Insufficient power for this spell"
        return wrapper
    return decorator


def retry_spell(
    max_attempts: int,
) -> Callable[
    [Callable[..., Any]],
    Callable[..., Any],
]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt < max_attempts:
                        msg = (
                            f"Retrying spell (attempt {attempt}/"
                            f"{max_attempts})"
                        )
                        print(msg)
                    else:
                        msg = (
                            f"Spell casting failed after {max_attempts} "
                            "attempts"
                        )
                        print(msg)
                        return msg
            return None
        return wrapper
    return decorator


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        stripped = name.strip()
        if len(stripped) < 3:
            return False
        if not any(c.isalpha() for c in stripped):
            return False
        return all(c.isalpha() or c.isspace() for c in stripped)

    @power_validator(10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


def main() -> None:
    print("Testing spell timer...")

    @spell_timer
    def fireball(target: str, power: int) -> str:
        time.sleep(0.1)
        return f"Fireball cast at {target}!"

    result = fireball("Dragon", 30)
    print(f"Result: {result}")
    print()

    print("Testing retrying spell...")
    attempt_counter = 0

    @retry_spell(3)
    def unstable_spell() -> str:
        nonlocal attempt_counter
        attempt_counter += 1
        if attempt_counter < 3:
            raise ValueError("Spell fizzled!")
        return "Waaaaaaagh spelled !"

    result = unstable_spell()
    print(f"Result: {result}")
    print()

    print("Testing MageGuild...")
    guild = MageGuild()

    res = MageGuild.validate_mage_name('Alice')
    print("validate_mage_name('Alice'):", res)

    res = MageGuild.validate_mage_name('A')
    print("validate_mage_name('A'):", res)

    res = MageGuild.validate_mage_name('John Doe')
    print("validate_mage_name('John Doe'):", res)

    res = MageGuild.validate_mage_name('   ')
    print("validate_mage_name('   '):", res)

    res = MageGuild.validate_mage_name('A B C')
    print("validate_mage_name('A B C'):", res)

    res = guild.cast_spell('Lightning', 15)
    print("cast_spell('Lightning', 15):", res)

    res = guild.cast_spell('Fireball', 5)
    print("cast_spell('Fireball', 5):", res)


if __name__ == "__main__":
    main()
