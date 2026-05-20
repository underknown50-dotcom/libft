def echo_validator(text: str) -> bool:
    cleaned = ''.join(ch.lower() for ch in text if ch.isalpha())

    if not cleaned:
        return False

    return cleaned == cleaned[::-1]
