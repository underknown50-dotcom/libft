def number_base_converter(number: str, from_base: int, to_base: int) -> str:
    degits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""

    if not (2 <= from_base <= 36) or not (2 <= to_base <= 36):
        return "ERROR"

    try:
        value = int(number, from_base)
    except ValueError:
        return "ERROR"

    if value == 0:
        return "0"

    while value > 0:
        result = degits[value % to_base] + result
        value = value // to_base

    return result


print(number_base_converter("0", 40, 10))
