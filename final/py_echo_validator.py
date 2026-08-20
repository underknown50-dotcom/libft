def echo_validator(text: str) -> bool:
    if not text:
        return False

    cleaned = [c.lower for c in text if c.isalpha()]

    return cleaned == cleaned[::-1]
