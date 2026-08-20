def string_sculptor(text: str) -> str:
    result = []
    index = 0

    for c in text:
        if c == " ":
            result.append(c)
            index = 0
        if c.isalpha():
            if index % 2 == 0:
                result.append(c.lower())
            else:
                result.append(c.upper())
            index += 1
        else:
            result.append(c)

    return "".join(result)
