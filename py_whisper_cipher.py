def whisper_cipher(text: str, shift: int) -> str:
    result = []
    for ch in text:
        if ch.isalpha():
            # Determine base character
            base = ord('a') if ch.islower() else ord('A')
            # Shift and wrap using modulo 26
            new_pos = (ord(ch) - base + shift) % 26
            result.append(chr(base + new_pos))
        else:
            result.append(ch)
    return ''.join(result)
