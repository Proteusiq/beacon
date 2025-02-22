from beacon.pan.fire import get_recommendation


def fry(text: str) -> list[dict[str, str]]:
    """Get book recommendations with both title and author."""
    return get_recommendation(text)
