from beacon.pan.fire import get_recommendation


def fry(text: str) -> list[str]:
    results = get_recommendation(text)
    return [r.metadata.get("title") for r in results]
