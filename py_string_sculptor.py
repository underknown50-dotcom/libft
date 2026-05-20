def string_sculptor(text: str) -> str:
    result = []
    make_lower = True   # first alphabetic should be lowercase

    for ch in text:
        if ch.isalpha():
            if make_lower:
                result.append(ch.lower())
            else:
                result.append(ch.upper())
            make_lower = not make_lower   # toggle for next alphabetic
        else:
            result.append(ch)

    return ''.join(result)
