from beacon.frier import bacons


def recommend(text: str) -> list[dict[str, str]]:
    """get personalized book recommendations based on text description.

    this is the main entry point for getting book recommendations.
    it uses semantic similarity to find books matching the input description.

    args:
        text: natural language description of desired book content
              examples:
              - "vampire love drama"
              - "detective solving murders in london"
              - "fantasy adventure with dragons"

    returns:
        list of dictionaries containing matched books with:
            - title: book title (including series info if applicable)
            - author: book author name

    example:
        >>> recommend("magical school for young wizards")
        [{'title': 'Harry Potter and the Sorcerer's Stone', 'author': 'J.K. Rowling'},
         ...]
    """
    return bacons.fry(text)
