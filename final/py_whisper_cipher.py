def whisper_cipher(text: str, shift: int) -> str:
    result = []

    for c in text:
        if c.isalpha():
            base = ord('A') if c.upper() else ord('a')
            shifted = (ord(c) - base + shift) % 26
            result.append(chr(base + shifted))
        else:
            result.append(c)

    return "".join(result)
