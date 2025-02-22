from beacon.frier import bacons


def recommend(text: str) -> list[dict[str, str]]:
    """Get book recommendations based on input text."""
    return bacons.fry(text)
