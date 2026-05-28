from .dark_spellbook import dark_spell_allowed_ingredients


def validate_ingredients(ingredients: str) -> str:
    allowed = dark_spell_allowed_ingredients()
    ing_lower = ingredients.lower()
    if any(a in ing_lower for a in allowed):
        return f"{ingredients} - VALID"
    else:
        return f"{ingredients} - INVALID"
