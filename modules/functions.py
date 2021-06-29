def reduce(text: str) -> str:
    text = "".join([c for c in text if ord(c) <= 128])
    resp = " "
    for i in text:
        if i == resp[-1]:
            continue
        else:
            resp += i
    resp = "".join(resp.lower().split())
    return resp