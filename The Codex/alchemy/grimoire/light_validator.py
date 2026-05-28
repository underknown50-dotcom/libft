def light_spell_allowed_ingredients() -> list[str]:
    return ["earth", "air", "fire", "water"]


def validate_ingredients(ingredients: str) -> str:
    allowed = light_spell_allowed_ingredients()
    ing_lower = ingredients.lower()
    if any(a in ing_lower for a in allowed):
        return f"{ingredients} - VALID"
    else:
        return f"{ingredients} - INVALID"
