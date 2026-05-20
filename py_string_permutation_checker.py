def string_permutation_checker(s1: str, s2: str) -> bool:
    if len(s1) != len(s2):
        return False

    freq = {}
    for ch in s1:
        freq[ch] = freq.get(ch, 0) + 1

    for ch in s2:
        if freq.get(ch, 0) == 0:
            return False
        freq[ch] -= 1

    return True
