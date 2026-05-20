def cryptic_sorter(strings: list[str]) -> list[str]:
    """
    Sorts a list of strings according to:
    1. Length (shortest first)
    2. Case‑insensitive ASCII order
    3. Number of vowels (ascending)
    Stable sort preserves original order for truly equal strings.
    """
    def vowel_count(s: str) -> int:
        # Count vowels (case‑insensitive)
        return sum(1 for ch in s if ch.lower() in "aeiou")

    # Python's sort is stable, and the key tuple defines the priority
    return sorted(strings, key=lambda s: (len(s), s.lower(), vowel_count(s)))
