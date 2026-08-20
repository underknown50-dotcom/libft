def anagram(s1: str, s2: str) -> bool:
    def normalize(s):
        return sorted(c.lower() for c in s if c != " ")

    return normalize(s1) == normalize(s2)
