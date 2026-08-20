def bracket_validator(s: str) -> bool:
    pairs = {')': '(', ']': '[', '}': '{'}
    opening = pairs.values()
    stack = []

    for ch in s:
        if ch in opening:
            stack.append(ch)
        elif not stack or stack.pop != pairs(ch):
            return False

    return not stack
