from collections.abc import Callable

# ----- 1. Mage Counter -----
def mage_counter() -> Callable[[], int]:
    count = 0
    def counter() -> int:
        nonlocal count
        count += 1
        return count
    return counter

# ----- 2. Spell Accumulator -----
def spell_accumulator(initial_power: int) -> Callable[[int], int]:
    total = initial_power
    def accumulate(amount: int) -> int:
        nonlocal total
        total += amount
        return total
    return accumulate

# ----- 3. Enchantment Factory -----
def enchantment_factory(enchantment_type: str) -> Callable[[str], str]:
    def enchant(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"
    return enchant

# ----- 4. Memory Vault -----
def memory_vault() -> dict[str, Callable]:
    storage = {}
    
    def store(key: str, value: any) -> None:
        storage[key] = value
    
    def recall(key: str) -> any:
        return storage.get(key, "Memory not found")
    
    return {'store': store, 'recall': recall}

# ----- Demonstration -----
if __name__ == "__main__":
    print("Testing mage counter...")
    counter_a = mage_counter()
    counter_b = mage_counter()
    
    print(f"counter_a call 1: {counter_a()}")  # 1
    print(f"counter_a call 2: {counter_a()}")  # 2
    print(f"counter_b call 1: {counter_b()}")  # 1 (independent)
    
    print("\nTesting spell accumulator...")
    acc = spell_accumulator(100)
    print(f"Base 100, add 20: {acc(20)}")      # 120
    print(f"Base 100, add 30: {acc(30)}")      # 150
    
    print("\nTesting enchantment factory...")
    flaming = enchantment_factory("Flaming")
    frozen = enchantment_factory("Frozen")
    print(flaming("Sword"))    # Flaming Sword
    print(frozen("Shield"))    # Frozen Shield
    
    print("\nTesting memory vault...")
    vault = memory_vault()
    vault['store']('secret', 42)
    print(f"Recall 'secret': {vault['recall']('secret')}")  # 42
    print(f"Recall 'unknown': {vault['recall']('unknown')}") # Memory not found