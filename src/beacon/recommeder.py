from beacon.frier import bacons


def recommend(text: str) -> list[str]:
    return bacons.fry(text)
