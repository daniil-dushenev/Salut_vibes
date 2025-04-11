from app.logger import logger

def validate_consistency(result: dict) -> dict:
    hair_type = result.get("hair_type")
    hair_length = result.get("hair_length")
    hair_color = result.get("hair_color")

    if hair_length == "Bald" or hair_type == "Bald" or hair_color == "Bald":
        if hair_type != "Bald":
            logger.debug(f"Conflict: hair_type='{hair_type}' → replaced with 'Bald'")
        if hair_length != "Bald":
            logger.debug(f"Conflict: hair_length='{hair_length}' → replaced with 'Bald'")
        if hair_color != "Bald":
            logger.debug(f"Conflict: hair_color='{hair_color}' → replaced with 'Bald'")
        result["hair_type"] = "Bald"
        result["hair_length"] = "Bald"
        result["hair_color"] = "Bald"

    return result

def check_semantic_warnings(result: dict) -> None:
    hair_color = result.get("hair_color")
    skin_color = result.get("skin_color")
    nationality = result.get("nationality")

    if hair_color == "Blonde hair" and skin_color == "Dark skin":
        logger.warning("Rare combination: 'Blonde hair' with 'Dark skin' — check validity.")

    if hair_color == "Red hair" and nationality in {"Indian", "African appearance", "Asian"}:
        logger.warning(f"Rare combination: 'Red hair' with '{nationality}' — may be incorrect.")

    if result.get("eye_color") == "Dark eyes" and skin_color == "Light skin":
        logger.debug("Interesting: 'Dark eyes' with 'Light skin'")

def validate_fields(result: dict) -> dict:
    REQUIRED_FIELDS = {
        "hair_color": [
            "Black hair", "Blonde hair", "Brown hair", "Red hair",
            "Gray hair", "Bald", "unknown"
        ],
        "eye_color": [
            "Brown eyes", "Blue eyes", "Green eyes", "Gray eyes", "Dark eyes", "unknown"
        ],
        "hair_length": [
            "Short hair", "Medium length hair", "Long hair", "Bald", "unknown"
        ],
        "hair_type": [
            "Straight hair", "Wavy hair", "Curly hair", "Dreadlocks", "Bald", "unknown"
        ],
        "skin_color": [
            "Light skin", "Tanned skin", "Dark skin", "Olive skin", "unknown"
        ],
        "lips": [
            "Full lips", "Thin lips", "Small lips", "Round lips", "unknown"
        ],
        "nationality": [
            "European", "African", "Asian", "Indian", "Caucasian", "unknown"
        ]
    }

    validated = {}
    changes = {}
    for field, allowed in REQUIRED_FIELDS.items():
        value = result.get(field, "unknown")
        if value not in allowed:
            logger.warning(f"Invalid value for {field}: '{value}' → replaced with 'unknown'")
            validated[field] = "unknown"
            changes[field] = {"from": value, "to": "unknown"}
        else:
            validated[field] = value

    if changes:
        logger.debug(f"Field corrections: {changes}")

    return validated

def run_all_validations(result: dict) -> dict:
    result = validate_fields(result)
    result = validate_consistency(result)
    check_semantic_warnings(result)
    return result