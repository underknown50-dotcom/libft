def pattern_tracker(text: str) -> int:
    count = 0

    for i in range(len(text - 1)):
        a, b = text[i], text[i + 1]
        if a.isalpha() and int(a) - int(b) == 1:
            count += 1

    return count
