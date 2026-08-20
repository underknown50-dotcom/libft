def inter(s1: str, s2: str) -> str:
    seen = set()
    result = []

    for c in s1:
        if c in s2 and c not in seen:
            result.append(c)
            seen.add(c)

    return "".join(result)
