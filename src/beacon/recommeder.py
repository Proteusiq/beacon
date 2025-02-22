from beacon.frier import becons


def recommend(text: str) -> list[str]:
    return becons.fry(text)
