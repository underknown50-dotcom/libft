from .light_validator import validate_ingredients


def light_spell_record(spell_name: str, ingredients: str) -> str:
    result = validate_ingredients(ingredients)
    return f"Spell recorded: {spell_name} ({result})"
