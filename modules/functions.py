def reduce(text: str) -> str:
    """Strips away much of a string

    In order, this function removes non-ASCII, removes
    characters duplicated more than twice, lowercases
    the string, and removes whitespace.
    """
    text = "".join([c for c in text if ord(c) <= 128])
    resp = "  "
    for i in text:
        if i == resp[-1] and i == resp[-2]:
            continue
        else:
            resp += i
    resp = "".join(resp.lower().split())
    return resp
