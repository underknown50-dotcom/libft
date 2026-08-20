def hidenp(small: str, big: str) -> bool:
    it = iter(big)
    return all(c in it for c in small)
