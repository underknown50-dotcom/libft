def bracket_validator(s: str) -> bool:
    matching = {')': '(', '}': '{', ']': '['}
    stack = []

    for ch in s:
        if ch in matching:
            if not stack:
                return False
            top = stack.pop()
            if top != matching[ch]:
                return False
        elif ch in matching.values():
            stack.append(ch)

    return not stack

def bracket_validator(s: str) -> bool:
    