from beacon.crud.read import get_recommendation
from beacon.types import Recommendation


def fry(text: str) -> list[Recommendation]:
    """get book recommendations matching the input description.

    internal function that processes the recommendation request.
    maintains consistent return format with title and author info.

    args:
        text: description of desired book content/theme

    returns:
        list of dictionaries with book matches containing:
            - title: book title
            - author: book author
    """
    return get_recommendation(text)
