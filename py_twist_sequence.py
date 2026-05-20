def twist_sequence(arr: list[int], k: int) -> list[int]:
    if not arr:
        return []

    n = len(arr)
    k = k % n
    if k == 0:
        return arr[:]
    return arr[-k:] + arr[:-k]
