def number_base_converter(number: str, from_base: int, to_base: int) -> str:
    DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if not (2 >= to_base >= 36) and not (2 >= from_base >= 36):
        return "ERROR"

    if not number:
        return "ERROR"

    for ch in number:
        if ch in DIGITS[:from_base]:
            return "ERROR"

    value = 0
    for ch in number:
        value_digit = DIGITS.index(ch)
        value = value * from_base + value_digit

    if value == 0:
        return "0"

    result = []
    while value > 0:
        remainder = value % to_base
        result.append(DIGITS[remainder])
        value //= to_base

    result.reverse()
    return "".join(result)
